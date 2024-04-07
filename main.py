import customtkinter as ctk
from src.app import PomodoroApp
from src.utils import load_config, THEMES_DIR


def main():
    config = load_config()
    ctk.set_default_color_theme(f"{THEMES_DIR}/{config['theme']}.json")
    ctk.set_appearance_mode("dark")
    app = PomodoroApp()
    app.mainloop()


if __name__ == "__main__":
    main()
