import os
import sys
import json
import customtkinter as ctk
from pygame import mixer


ctk.set_appearance_mode("dark")

mixer.init()
beep = mixer.Sound('beep.mp3')
beep.set_volume(0.05)


def save_theme(theme):
    config = load_config()
    config['theme'] = theme
    save_config(config)

def load_config():
    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        config = {'theme': 'Default'}
    
    ctk.set_default_color_theme(f"themes/{config['theme']}.json")

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


class SettingsFrame(ctk.CTkFrame):
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

    def change_theme(self, theme):
        save_theme(theme)
        reload_app()

class PomodoroFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data_file = 'data.json'
        self.pomodoro_time = 25 * 60

        minutes, seconds = divmod(self.pomodoro_time, 60)
        self.timer_display = ctk.CTkLabel(self, text=f"{minutes:02d}:{seconds:02d}", font=("Helvetica", 58))
        self.timer_display.pack(pady=40)

        self.start_button = ctk.CTkButton(self, text="START", fg_color="transparent",
                                          border_width=2, command=self.start_timer)
        self.start_button.pack()

        self.running = False
        self.remaining_time = self.pomodoro_time

    def start_timer(self):
        self.running = not self.running
        btn_text = "PAUSE" if self.running else "START"
        self.start_button.configure(text=btn_text)
        if self.running:
            self.update_timer()

    def update_timer(self):
        if self.running and self.remaining_time > 0:
            self.remaining_time -= 1
            self.track_second()
            minutes, seconds = divmod(self.remaining_time, 60)
            self.timer_display.configure(text=f"{minutes:02d}:{seconds:02d}")
            self.after(1000, self.update_timer)
        elif self.remaining_time == 0:
            self.running = False
            self.session_ended()
        else:
            self.running = False

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
        # Reset the timer
        self.remaining_time = self.pomodoro_time
        minutes, seconds = divmod(self.remaining_time, 60)
        self.timer_display.configure(text=f"{minutes:02d}:{seconds:02d}")
        self.start_button.configure(text="START")

        # Update the total pomodoro sessions done
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                data['total_pomodoro_sessions_done'] = data.get('total_pomodoro_sessions_done', 0) + 1

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
    load_config()
    app = PomodoroApp()
    app.mainloop()
