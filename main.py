import os
import sys
import json
import customtkinter as ctk
from datetime import datetime
from pygame import mixer

BREAK_BTN_COLOR = "#9a9a9a"
BREAK_HOVER = "#adaaaa"
RESET_BTN_COLOR = "#bd9909"
RESET_HOVER = "#dbb30f"

DEF_POMODORO_MINS = 25
DEF_SB_MINS = 5
DEF_LB_MINS = 10

mixer.init()
beep = mixer.Sound('beep.mp3')


def load_config():
    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        config = {'theme': 'Default'}

    return config

def save_config(config):
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file)

def reload_app():
    os.execl(sys.executable, sys.executable, *sys.argv)


class StatsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data_file = 'data.json'

        self.total_today_var = ctk.StringVar(value="Pomodoros Today:  0")
        self.total_today = ctk.CTkLabel(self, textvariable=self.total_today_var, 
                                              font=("Helvetica", 16, "bold"), anchor="w")
        self.total_today.pack(padx=20, pady=(20, 0), fill="x")

        self.total_hours_var = ctk.StringVar(value="Total Hours Studied:  0")
        self.total_hours = ctk.CTkLabel(self, textvariable=self.total_hours_var, 
                                              font=("Helvetica", 16, "bold"), anchor="w")
        self.total_hours.pack(padx=20, pady=(20, 0), fill="x")

        self.total_var = ctk.StringVar(value="Total Pomodoros:  0")
        self.total = ctk.CTkLabel(self, textvariable=self.total_var, 
                                              font=("Helvetica", 16, "bold"), anchor="w")
        self.total.pack(padx=20, pady=(20, 0), fill="x")

        self.update_stats = ctk.CTkButton(self, text="Update", width=90, font=("Roboto", 16), command=self.load_stats)
        self.update_stats.pack(pady=40, side=ctk.BOTTOM)

        self.load_stats()

    def load_stats(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                current_date = datetime.now().strftime("%Y-%m-%d")
                total_today = data.get('sessions_by_date', {}).get(current_date, 0)

                self.total_today_var.set(f"Pomodoros Today:  {total_today}")

                total_seconds_studied = data.get('total_seconds_studied', 0)
                total_hours = total_seconds_studied / 3600

                self.total_hours_var.set(f"Total Hours Studied:  {total_hours:.1f}")

                self.total_var.set(f"Total Pomodoros:  {data.get('total_pomodoro_sessions', 0)}")


class EntryFrame(ctk.CTkFrame):
    def __init__(self, master, text, config_attr, defvalue, command):
        super().__init__(master)

        self.label = ctk.CTkLabel(self, text=text)
        self.label.pack(pady=(10, 10), padx=(10, 10))

        # Inner frame to hold the entry and button
        self.controls_frame = ctk.CTkFrame(self)
        self.controls_frame.pack(fill=ctk.X, expand=True, padx=10)

        self.entry_var = ctk.IntVar(value=config.get(config_attr, defvalue))
        self.entry = ctk.CTkEntry(self.controls_frame, width=35, textvariable=self.entry_var)
        self.entry.pack(side=ctk.LEFT, fill=ctk.X, expand=True, padx=(0, 10))

        self.set_button = ctk.CTkButton(self.controls_frame, width=120, text="Set", command=command)
        self.set_button.pack(side=ctk.RIGHT)

    def get(self):
        return self.entry_var.get()


class SettingsFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.themes_dir = 'themes'
        config = load_config()

        # Pomodoro Duration
        self.pomodoro_entry = EntryFrame(self, "Pomodoro Duration (mins):", "pomodoro_time", DEF_POMODORO_MINS, self.change_pomodoro_time)
        self.pomodoro_entry.pack()

        # Short Break Duration
        self.sb_entry = EntryFrame(self, "Short Break Duration (mins):", "short_break_time", DEF_SB_MINS, self.change_sb_time)
        self.sb_entry.pack(pady=(5, 0))

        # Long Break Duration
        self.lb_entry = EntryFrame(self, "Long Break Duration (mins):", "long_break_time", DEF_LB_MINS, self.change_lb_time)
        self.lb_entry.pack(pady=(5, 0))

        # Selecting theme
        self.theme_label = ctk.CTkLabel(self, text="Select Theme:")
        self.theme_label.pack(pady=(20, 0))

        self.theme_options = [os.path.splitext(theme)[0] for theme in os.listdir(self.themes_dir) if theme.endswith('.json')]

        selected = ctk.StringVar(value=config.get('theme', 'Default'))        
        self.theme_menu = ctk.CTkOptionMenu(self, variable=selected, values=self.theme_options, anchor="n", command=self.change_theme)
        self.theme_menu.pack(pady=(10, 0))

        # Volume Slider
        self.volume_label = ctk.CTkLabel(self, text="Adjust Beep Volume:")
        self.volume_label.pack(pady=(20, 0))

        self.volume_slider = ctk.CTkSlider(self, from_=0, to=100, number_of_steps=100, command=self.change_volume)
        self.volume_slider.pack(pady=(10, 0))

        # Set the slider to the current volume
        self.volume_slider.set(config.get('volume', 10))  # Default volume to 10% if not set
        self.change_volume(config.get('volume', 10))

        # Play Beep button
        self.beep_button = ctk.CTkButton(self, text="Play", width=70, command=beep.play)
        self.beep_button.pack(pady=(15, 0))

    def change_time(self, entry, config_param):
        time = entry.get()
        if time and time > 0:
            config = load_config()
            config[config_param] = time
            save_config(config)

    def change_pomodoro_time(self):
        self.change_time(self.pomodoro_entry, "pomodoro_time")

    def change_sb_time(self):
        self.change_time(self.sb_entry, "short_break_time")

    def change_lb_time(self):
        self.change_time(self.lb_entry, "long_break_time")

    def change_theme(self, theme):
        config = load_config()
        config['theme'] = theme
        save_config(config)
        reload_app()

    def change_volume(self, volume):
        volume = float(volume) / 100
        beep.set_volume(volume)
        config = load_config()
        config['volume'] = volume * 100
        save_config(config)


class PomodoroFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data_file = 'data.json'
        config = load_config()
        # TODO: fix crutch
        self.pomodoro_time = config.get("pomodoro_time", 25) * 60

        minutes, seconds = divmod(self.pomodoro_time, 60)
        self.timer_display = ctk.CTkLabel(self, text=f"{minutes:02d}:{seconds:02d}", font=("Helvetica", 58))
        self.timer_display.pack(pady=40)

        self.start_button = ctk.CTkButton(self, text="Start", font=("Roboto", 17), border_width=2, command=self.start_timer)
        self.start_color = self.start_button.cget("fg_color")
        self.start_button.pack(pady=(0, 10))

        self.sb_button = ctk.CTkButton(self, text="Short break", font=("Roboto", 17), fg_color=BREAK_BTN_COLOR, hover_color=BREAK_HOVER, command=self.short_break)
        self.sb_button.pack(pady=(0, 10))

        self.lb_button = ctk.CTkButton(self, text="Long break", font=("Roboto", 17), fg_color=BREAK_BTN_COLOR, hover_color=BREAK_HOVER, command=self.long_break)
        self.lb_button.pack(pady=(0, 10))

        self.reset_button = ctk.CTkButton(self, text="Reset", font=("Roboto", 17), fg_color=RESET_BTN_COLOR, hover_color=RESET_HOVER, command=self.reset)
        self.reset_button.pack()

        self.running = False
        self.next_timer_update = None
        self.remaining_time = self.pomodoro_time

    def start_timer(self):
        if self.next_timer_update:
            self.after_cancel(self.next_timer_update)

        self.running = not self.running
        btn_text = "Pause" if self.running else "Resume"
        btn_fg = "transparent" if self.running else self.start_color
        self.start_button.configure(text=btn_text, fg_color=btn_fg, hover=not self.running)
        self.update_timer()

    def update_timer(self):
        if self.running and self.remaining_time > 0:
            self.remaining_time -= 1
            self.track_second()
            minutes, seconds = divmod(self.remaining_time, 60)
            self.timer_display.configure(text=f"{minutes:02d}:{seconds:02d}")
            self.next_timer_update = self.after(1000, self.update_timer)
        elif self.remaining_time == 0:
            self.session_ended()

    def track_second(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                data['total_seconds_studied'] += 1
        else:
            data = {'total_seconds_studied': 0}
        
        with open(self.data_file, 'w') as file:
            json.dump(data, file, indent=4)

    def reset(self, to:str="pomodoro_time", default:int=25):
        self.running = False
        if self.next_timer_update:
            self.after_cancel(self.next_timer_update)
            self.next_timer_update = None

        config = load_config()
        # TODO: fix crutch
        self.pomodoro_time = int(config.get(to, default) * 60)

        # Reset the timer
        self.remaining_time = self.pomodoro_time
        minutes, seconds = divmod(self.remaining_time, 60)
        self.timer_display.configure(text=f"{minutes:02d}:{seconds:02d}")
        self.start_button.configure(text="Start", fg_color=self.start_color)

    def session_ended(self):
        self.reset()
 
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

        beep.play() 

    def short_break(self):
        self.reset(to="short_break_time", default=5)
        self.start_timer()
    
    def long_break(self):
        self.reset(to="long_break_time", default=10)
        self.start_timer()


class TabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.add("Main")
        self.add("Settings")
        self.add("Stats")

        self.main_frame = PomodoroFrame(self.tab("Main"))
        self.main_frame.pack(expand=True, fill='both')

        self.settings_frame = SettingsFrame(self.tab("Settings"))
        self.settings_frame.pack(expand=True, fill='both')

        self.stats_frame = StatsFrame(self.tab("Stats"))
        self.stats_frame.pack(expand=True, fill='both')


class PomodoroApp(ctk.CTk):
    WIDTH = 350
    HEIGHT = 400

    def __init__(self):
        super().__init__()

        self.title("Pomodoro Tracker")
        self.geometry(f"{PomodoroApp.WIDTH}x{PomodoroApp.HEIGHT}")

        self.tabview = TabView(master=self)
        self.tabview.pack(pady=(15, 30), expand=True, fill='y')


if __name__ == "__main__":
    config = load_config()
    ctk.set_default_color_theme(f"themes/{config['theme']}.json")
    ctk.set_appearance_mode("dark")
    app = PomodoroApp()
    app.mainloop()
