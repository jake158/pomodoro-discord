import os
import json
import time
import threading
import customtkinter as ctk
from datetime import datetime, timedelta
from src.utils import load_config, DEF_POMODORO_MINS, DEF_SB_MINS, DEF_LB_MINS, beep
from src.richpresence import RichPresence

BREAK_BTN_COLOR = "#9a9a9a"
BREAK_HOVER = "#adaaaa"
RESET_BTN_COLOR = "#bd9909"
RESET_HOVER = "#dbb30f"


class PomodoroFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data_file = 'data.json'
        config = load_config()

        # Rich presence in separate thread
        threading.Thread(target=self.init_rpc, daemon=True).start()

        # Helper text that appears when a break is running
        self.break_text = ctk.StringVar(value="")
        self.break_label = ctk.CTkLabel(self, textvariable=self.break_text, font=("Roboto", 15))
        self.break_label.pack(pady=(5, 0))

        # Display
        self.pomodoro_time = config.get("pomodoro_time", DEF_POMODORO_MINS) * 60

        minutes, seconds = divmod(self.pomodoro_time, 60)
        self.timer_display = ctk.CTkLabel(self, text=f"{minutes:02d}:{seconds:02d}", font=("Helvetica", 58))
        self.timer_display.pack(pady=(15, 41))

        # Controls
        self.start_button = ctk.CTkButton(self, text="Start", font=("Roboto", 17), border_width=2, command=self.start_timer)
        self.start_color = self.start_button.cget("fg_color")
        self.start_button.pack(pady=(0, 10))

        self.sb_button = ctk.CTkButton(self, text="Short break", font=("Roboto", 17), fg_color=BREAK_BTN_COLOR, hover_color=BREAK_HOVER, command=self.short_break)
        self.sb_button.pack(pady=(0, 10))

        self.lb_button = ctk.CTkButton(self, text="Long break", font=("Roboto", 17), fg_color=BREAK_BTN_COLOR, hover_color=BREAK_HOVER, command=self.long_break)
        self.lb_button.pack(pady=(0, 10))

        self.reset_button = ctk.CTkButton(self, text="Reset", font=("Roboto", 17), fg_color=RESET_BTN_COLOR, hover_color=RESET_HOVER, command=self.reset)
        self.reset_button.pack()

        # State
        self.running = False
        self.break_running = False
        self.next_timer_update = None
        self.remaining_time = self.pomodoro_time
        # States used for Rich Presence
        self.start_time_timestamp = None
        self.end_time_timestamp = None
        self.session_counter = 0

    def init_rpc(self):
        self.rpc = RichPresence()
        self.rpc_thread = threading.Thread(target=self.update_rpc, daemon=True)
        self.rpc_thread.start()

    def update_rpc(self):
        while True:
            if self.break_running:
                self.rpc.break_state(self.start_time_timestamp, self.end_time_timestamp)
            elif self.running:
                self.rpc.running_state(self.session_counter + 1, self.start_time_timestamp, self.end_time_timestamp)
            else:
                self.rpc.default_state()

            # Discord-imposed rate limit
            time.sleep(15)

    def start_timer(self):
        if self.next_timer_update:
            self.after_cancel(self.next_timer_update)

        # Rich presence info
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=self.remaining_time)
        self.start_time_timestamp = start_time.timestamp()
        self.end_time_timestamp = end_time.timestamp()

        self.running = not self.running
        btn_text = "Pause" if self.running else "Resume"
        btn_fg = "transparent" if self.running else self.start_color
        self.start_button.configure(text=btn_text, fg_color=btn_fg, hover=not self.running)
        self.update_timer()

    def update_timer(self):
        if self.running and self.remaining_time > 0:
            self.remaining_time -= 1
            if not self.break_running:
                self.track_second()
            minutes, seconds = divmod(self.remaining_time, 60)
            self.timer_display.configure(text=f"{minutes:02d}:{seconds:02d}")
            self.next_timer_update = self.after(1000, self.update_timer)
        elif self.remaining_time == 0:
            self.session_ended()

    def track_second(self):
        # TODO: I don't like the if check every second
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                data['total_seconds_studied'] += 1
        else:
            data = {'total_seconds_studied': 0}
        
        with open(self.data_file, 'w') as file:
            json.dump(data, file, indent=4)

    def reset(self, to:str="pomodoro_time", default:int=DEF_POMODORO_MINS):
        self.running = False
        self.break_running = False
        self.break_text.set("")

        if self.next_timer_update:
            self.after_cancel(self.next_timer_update)
            self.next_timer_update = None

        config = load_config()
        # TODO: Make cleaner?
        self.pomodoro_time = int(config.get(to, default) * 60)

        # Reset the timer
        self.remaining_time = self.pomodoro_time
        minutes, seconds = divmod(self.remaining_time, 60)
        self.timer_display.configure(text=f"{minutes:02d}:{seconds:02d}")
        self.start_button.configure(text="Start", fg_color=self.start_color)

    def session_ended(self):
        was_break = self.break_running
        # Reset sets break_running to false
        # TODO: surely there is a better way

        self.reset()
        beep.play() 

        if was_break:
            return

        self.session_counter += 1
 
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                data['total_pomodoro_sessions'] = data.get('total_pomodoro_sessions', 0) + 1

                if 'sessions_by_date' not in data:
                    data['sessions_by_date'] = {}
                data['sessions_by_date'][current_date] = data['sessions_by_date'].get(current_date, 0) + 1
        else:
            data = {
                'total_seconds_studied': 0, 
                'total_pomodoro_sessions': 1,
                'sessions_by_date': {current_date: 1}
            }
        
        with open(self.data_file, 'w') as file:
            json.dump(data, file, indent=4)


    def short_break(self):
        self.reset(to="short_break_time", default=DEF_SB_MINS)
        self.break_running = True
        self.break_text.set("Short break")
        self.start_timer()
    
    def long_break(self):
        self.reset(to="long_break_time", default=DEF_LB_MINS)
        self.break_running = True
        self.break_text.set("Long break")
        self.start_timer()
