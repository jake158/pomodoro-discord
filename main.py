import os
import sys
import json
import customtkinter as ctk


ctk.set_appearance_mode("dark")


def save_theme(theme):
    config = {'selected_theme': theme}
    with open('theme.json', 'w') as config_file:
        json.dump(config, config_file)

def load_theme():
    try:
        with open('theme.json', 'r') as config_file:
            config = json.load(config_file)
            selected_theme = config.get('selected_theme', 'Default')
    except FileNotFoundError:
        selected_theme = 'Default'

    ctk.set_default_color_theme(f"themes/{selected_theme}.json")


def reload_app():
    os.execl(sys.executable, sys.executable, *sys.argv)


class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.theme_label = ctk.CTkLabel(self, text="Select Theme:")
        self.theme_label.pack(pady=10)

        themes_dir = 'themes'
        self.theme_options = [os.path.splitext(theme)[0] for theme in os.listdir(themes_dir) if theme.endswith('.json')]
        
        self.theme_var = ctk.StringVar(value="...")

        self.theme_menu = ctk.CTkOptionMenu(self, variable=self.theme_var, values=self.theme_options, anchor="n", command=self.change_theme)
        self.theme_menu.pack()

    def change_theme(self, theme):
        save_theme(theme)
        reload_app()


class PomodoroFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.timer_display = ctk.CTkLabel(self, text="25:00", font=("Helvetica", 58))
        self.timer_display.pack(pady=50)

        self.start_button = ctk.CTkButton(self, text="Start", fg_color="transparent",
                                          border_width=2, command=self.start_timer)
        self.start_button.pack()

    def start_timer(self):
        print("Timer started")


class TabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.add("Main")
        self.add("Settings")

        self.main_frame = PomodoroFrame(self.tab("Main"))
        self.main_frame.pack()

        self.settings_frame = SettingsFrame(self.tab("Settings"))
        self.settings_frame.pack()


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
    load_theme()
    app = PomodoroApp()
    app.mainloop()
