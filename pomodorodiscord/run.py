import customtkinter as ctk
from src.app import PomodoroApp
from src.utils import load_config

if __name__ == "__main__":
    config = load_config()
    ctk.set_default_color_theme(f"themes/{config['theme']}.json")
    ctk.set_appearance_mode("dark")
    app = PomodoroApp()
    app.mainloop()
