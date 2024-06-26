import time
import threading
import customtkinter as ctk
from datetime import datetime, timedelta
from CTkMessagebox import CTkMessagebox
from src.utils import load_config, load_data, save_data, beep, DEF_POMODORO_MINS, DEF_SB_MINS, DEF_LB_MINS, DEF_SB_BEFORE_L
from src.logic.richpresence import RichPresence

BREAK_BTN_COLOR = "#9a9a9a"
BREAK_HOVER = "#adaaaa"
RESET_BTN_COLOR = "#cca508"
RESET_HOVER = "#e3b707"
CONNECTED_TEXT = "Connected to Discord"
CONNECTED_COLOR = "gray65"
CONNECTED_HOVER = "gray77"
DISCONNECTED_TEXT = "Not connected to Discord"
DISCONNECTED_COLOR = "#d93b3b"
DISCONNECTED_HOVER = "#fa5757"


class PomodoroFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        config = load_config()
        self.initialize_ui(config)
        self.initialize_state(config)
        threading.Thread(target=self.initialize_rpc, daemon=True).start()

    def initialize_ui(self, config):
        # Helper text that appears when a break is running
        self.break_text     = ctk.StringVar(value="")
        self.break_label    =  ctk.CTkLabel(self,
                                            textvariable=self.break_text,
                                            font=("Roboto", 15))

        # Display
        self.pomodoro_time = config.get("pomodoro_time", DEF_POMODORO_MINS) * 60
        minutes, seconds = divmod(self.pomodoro_time, 60)
        self.timer_display  =  ctk.CTkLabel(self,
                                            text=f"{minutes:02d}:{seconds:02d}",
                                            font=("Helvetica", 58))

        # Controls
        self.start_button   = ctk.CTkButton(self,
                                            text="Start",
                                            font=("Roboto", 17),
                                            border_width=2,
                                            command=self.toggle_timer)
        # Used in toggle_timer()
        self.start_color = self.start_button.cget("fg_color")

        self.sb_button      = ctk.CTkButton(self,
                                            text="Short break",
                                            font=("Roboto", 17),
                                            fg_color=BREAK_BTN_COLOR,
                                            hover_color=BREAK_HOVER,
                                            command=self.short_break)

        self.lb_button      = ctk.CTkButton(self,
                                            text="Long break",
                                            font=("Roboto", 17),
                                            fg_color=BREAK_BTN_COLOR,
                                            hover_color=BREAK_HOVER,
                                            command=self.long_break)

        self.reset_button   = ctk.CTkButton(self,
                                            text="Reset",
                                            font=("Roboto", 17),
                                            fg_color=RESET_BTN_COLOR,
                                            hover_color=RESET_HOVER,
                                            command=self.reset)

        self.discord_button = ctk.CTkButton(self,
                                            text="Connecting...",
                                            font=("Roboto", 12),
                                            fg_color="transparent",
                                            text_color=CONNECTED_COLOR,
                                            width=70,
                                            hover_color=self.cget("bg_color"),
                                            command=self.toggle_rpc,
                                            state="disabled")

        # Make text change color on hover
        self.discord_button.bind("<Enter>",
                                  lambda e: self.discord_button.configure(text_color=CONNECTED_HOVER
                                                                          if self.discord_button.cget("text") is not DISCONNECTED_TEXT
                                                                          else DISCONNECTED_HOVER))
        self.discord_button.bind("<Leave>", 
                                  lambda e: self.discord_button.configure(text_color=CONNECTED_COLOR
                                                                          if self.discord_button.cget("text") is not DISCONNECTED_TEXT
                                                                          else DISCONNECTED_COLOR))

        self.break_label.pack(pady=(5, 0))
        self.timer_display.pack(pady=(15, 41))
        self.start_button.pack(pady=(0, 10))
        self.sb_button.pack(pady=(0, 10))
        self.lb_button.pack(pady=(0, 10))
        self.reset_button.pack(pady=(0, 10))
        self.discord_button.pack(pady=(27, 0))

    def initialize_state(self, config):
        self.running = False
        self.break_running = False
        self.next_timer_update = None
        self.remaining_time = self.pomodoro_time

        # Tracking time studied today in track_second()
        self.current_date = datetime.now().strftime("%Y-%m-%d")

        # Automatic break cycling
        self.auto_break_cycling = config.get("auto_break_cycling", False)
        self.short_breaks_before_long = config.get("short_breaks_before_long", DEF_SB_BEFORE_L)
        self.short_break_running = False
        self.short_break_counter = 0

        # Rich Presence
        self.start_time_timestamp = None
        self.end_time_timestamp = None
        self.session_counter = 0
        self.seconds_studied = 0
        self.paused = False

    def initialize_rpc(self):
        self.rpc = RichPresence()
        self.discord_button.configure(state="normal", text=CONNECTED_TEXT)
        self.rpc_thread = threading.Thread(target=self.update_rpc, daemon=True)
        self.rpc_thread.start()

    def toggle_rpc(self):
        self.discord_button.configure(state="disabled")
        if not self.rpc.connected:
            self.discord_button.configure(text="Connecting...")
            threading.Thread(target=self.connect_rpc, daemon=True).start()
        else:
            self.discord_button.configure(text="Disconnecting...")
            threading.Thread(target=self.disconnect_rpc, daemon=True).start()

    def connect_rpc(self):
        if self.rpc.connect():
            self.discord_button.configure(text=CONNECTED_TEXT, text_color=CONNECTED_COLOR, state="normal")
        else:
            self.discord_button.configure(text=DISCONNECTED_TEXT, text_color=DISCONNECTED_COLOR, state="normal")
            CTkMessagebox(title="Error", message="Connecting to Discord failed. Check console for error output", icon="cancel")

    def disconnect_rpc(self):
        if self.rpc.disconnect():
            self.discord_button.configure(text=DISCONNECTED_TEXT, text_color=DISCONNECTED_COLOR, state="normal")
        else:
            self.discord_button.configure(text=CONNECTED_TEXT, text_color=CONNECTED_COLOR, state="normal")
            CTkMessagebox(title="Error", message="Disconnecting from Discord failed. Check console for error output", icon="cancel")

    def update_rpc(self):
        while True:
            if self.rpc.connected:
                if self.break_running:
                    self.rpc.break_state(self.seconds_studied, self.start_time_timestamp, self.end_time_timestamp)
                elif self.running:
                    self.rpc.running_state(self.session_counter + 1, self.start_time_timestamp, self.end_time_timestamp)
                elif self.paused:
                    self.rpc.paused_state(self.start_time_timestamp)
                else:
                    self.rpc.idling_state(self.seconds_studied)
            elif self.discord_button.cget("state") == 'normal':
                self.discord_button.configure(text=DISCONNECTED_TEXT, text_color=DISCONNECTED_COLOR)

            # Discord-imposed rate limit
            time.sleep(15)

    def toggle_timer(self):
        if self.next_timer_update:
            self.after_cancel(self.next_timer_update)
        self.running = not self.running
        btn_text = "Pause" if self.running else "Resume"
        btn_fg = "transparent" if self.running else self.start_color
        self.start_button.configure(text=btn_text, fg_color=btn_fg, hover=not self.running)

        # Tracking time studied today in track_second()
        now = datetime.now()
        self.current_date = now.strftime("%Y-%m-%d")
        # Rich presence info
        end_time = now + timedelta(seconds=self.remaining_time)
        self.start_time_timestamp = now.timestamp()
        self.end_time_timestamp = end_time.timestamp()
        self.paused = not self.running

        self.update_timer()

    def update_timer(self):
        if self.running and self.remaining_time > 0:
            self.next_timer_update = self.after(1000, self.update_timer)
            self.remaining_time -= 1
            if not self.break_running:
                self.track_second()
            minutes, seconds = divmod(self.remaining_time, 60)
            self.timer_display.configure(text=f"{minutes:02d}:{seconds:02d}")
        elif self.remaining_time == 0:
            self.session_ended()

    def track_second(self):
        self.seconds_studied += 1
        data = load_data()
        data['total_seconds_studied'] += 1
        data['seconds_by_date'][self.current_date] = data['seconds_by_date'].get(self.current_date, 0) + 1
        save_data(data)

    def session_ended(self):
        self.short_break_counter += 1 if self.short_break_running else 0
        was_break = self.break_running
        self.session_counter += 1 if not was_break else 0
        self.reset()
        beep.play()

        if was_break and self.auto_break_cycling:
            self.toggle_timer()
        elif not was_break:
            self.pomodoro_complete()

    def reset(self, to: str = "pomodoro_time", default: int = DEF_POMODORO_MINS):
        if self.next_timer_update:
            self.after_cancel(self.next_timer_update)
            self.next_timer_update = None

        self.running = False
        self.break_running = False
        self.short_break_running = False
        self.paused = False
        self.break_text.set("")

        # Load current settings
        config = load_config()
        self.pomodoro_time = int(config.get(to, default) * 60)
        self.auto_break_cycling = config.get("auto_break_cycling", False)
        self.short_break_counter = 0 if not self.auto_break_cycling else self.short_break_counter
        self.short_breaks_before_long = config.get("short_breaks_before_long", DEF_SB_BEFORE_L)

        # Reset the timer
        self.remaining_time = self.pomodoro_time
        minutes, seconds = divmod(self.remaining_time, 60)
        self.timer_display.configure(text=f"{minutes:02d}:{seconds:02d}")
        self.start_button.configure(text="Start", fg_color=self.start_color)

    def pomodoro_complete(self):
        data = load_data()
        data['total_pomodoro_sessions'] += 1
        data['sessions_by_date'][self.current_date] = data['sessions_by_date'].get(self.current_date, 0) + 1
        save_data(data)

        if self.auto_break_cycling:
            if self.short_break_counter >= self.short_breaks_before_long:
                self.short_break_counter = 0
                self.long_break()
            else:
                self.short_break()

    def short_break(self):
        self.reset(to="short_break_time", default=DEF_SB_MINS)
        self.break_running = True
        self.short_break_running = True
        self.break_text.set("Short break")
        self.toggle_timer()

    def long_break(self):
        self.reset(to="long_break_time", default=DEF_LB_MINS)
        self.break_running = True
        self.break_text.set("Long break")
        self.toggle_timer()
