import os
import sys
import json
import customtkinter as ctk
from datetime import datetime
from pygame import mixer


ctk.set_appearance_mode("dark")

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

        self.total_hours_var = ctk.StringVar(value="Total Hours Studied: 0")
        self.total_hours_label = ctk.CTkLabel(self, textvariable=self.total_hours_var, font=("Helvetica", 18, "bold"))
        self.total_hours_label.pack(pady=40)

        self.load_stats()

    def load_stats(self):
        # TODO: Implement
        self.total_hours_var.set("Total Hours Studied: ...")

    def update_stats(self, new_data):
        # TODO: Implement
        pass


class SettingsFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.select_var = ctk.StringVar(value="...")

        # Selecting theme
        self.theme_label = ctk.CTkLabel(self, text="Select Theme:")
        self.theme_label.pack(pady=10)

        themes_dir = 'themes'
        self.theme_options = [os.path.splitext(theme)[0] for theme in os.listdir(themes_dir) if theme.endswith('.json')]
        
        self.theme_menu = ctk.CTkOptionMenu(self, variable=self.select_var, values=self.theme_options, anchor="n", command=self.change_theme)
        self.theme_menu.pack()

        # Volume Slider
        self.volume_label = ctk.CTkLabel(self, text="Adjust Beep Volume:")
        self.volume_label.pack(pady=(20, 2))

        self.volume_slider = ctk.CTkSlider(self, from_=0, to=100, number_of_steps=100, command=self.change_volume)
        self.volume_slider.pack(pady=20)

        # Set the slider to the current volume
        config = load_config()
        self.volume_slider.set(config.get('volume', 10))  # Default volume to 10% if not set
        self.change_volume(config.get('volume', 10))

        # Play Beep button
        self.beep_button = ctk.CTkButton(self, text="Play", fg_color="transparent",
                                          border_width=2, width=70, command=beep.play)
        self.beep_button.pack()

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
        self.pomodoro_time = 25 * 60

        minutes, seconds = divmod(self.pomodoro_time, 60)
        self.timer_display = ctk.CTkLabel(self, text=f"{minutes:02d}:{seconds:02d}", font=("Helvetica", 58))
        self.timer_display.pack(pady=40)

        self.start_button = ctk.CTkButton(self, text="Start", font=("Roboto", 17), border_width=2, command=self.start_timer)
        self.start_color = self.start_button.cget("fg_color")
        self.start_button.pack()

        self.running = False
        self.next_timer_update = None
        self.remaining_time = self.pomodoro_time

    def start_timer(self):
        if self.next_timer_update:
            # Prevents two update_timer loops happening at the same time
            self.after_cancel(self.next_timer_update)

        self.running = not self.running
        btn_text = "Pause" if self.running else "Start"
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

    def session_ended(self):
        self.running = False
        self.next_timer_update = None

        # Reset the timer
        self.remaining_time = self.pomodoro_time
        minutes, seconds = divmod(self.remaining_time, 60)
        self.timer_display.configure(text=f"{minutes:02d}:{seconds:02d}")
        self.start_button.configure(text="START")
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Update the total pomodoro sessions done and sessions done per date
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                data['total_pomodoro_sessions_done'] = data.get('total_pomodoro_sessions_done', 0) + 1

                if 'sessions_by_date' not in data:
                    data['sessions_by_date'] = {}
                data['sessions_by_date'][current_date] = data['sessions_by_date'].get(current_date, 0) + 1
        else:
            data = {
                'total_seconds_studied': 0, 
                'total_pomodoro_sessions_done': 1,
                'sessions_by_date': {current_date: 1}
            }
        
        with open(self.data_file, 'w') as file:
            json.dump(data, file, indent=4)

        beep.play() 


class TabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.add("Main")
        self.add("Settings")
        self.add("Stats")

        self.main_frame = PomodoroFrame(self.tab("Main"))
        self.main_frame.pack()

        self.settings_frame = SettingsFrame(self.tab("Settings"))
        self.settings_frame.pack()

        self.stats_frame = StatsFrame(self.tab("Stats"))
        self.stats_frame.pack()


class PomodoroApp(ctk.CTk):
    WIDTH = 350
    HEIGHT = 350

    def __init__(self):
        super().__init__()

        self.title("Pomodoro Tracker")
        self.geometry(f"{PomodoroApp.WIDTH}x{PomodoroApp.HEIGHT}")

        self.tabview = TabView(master=self)
        self.tabview.pack(pady=30)


if __name__ == "__main__":
    config = load_config()
    ctk.set_default_color_theme(f"themes/{config['theme']}.json")
    app = PomodoroApp()
    app.mainloop()
