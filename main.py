import os
import customtkinter as ctk
from src.app import PomodoroApp
from src.utils import load_config, THEMES_DIR


data_dir = os.path.dirname(__file__)


def main():
    config = load_config()
    ctk.set_default_color_theme(os.path.join(data_dir, THEMES_DIR, f"{config['theme']}.json"))
    ctk.set_appearance_mode("dark")
    icon_path = os.path.join(data_dir, 'src', 'assets', 'icon.png')
    app = PomodoroApp(icon_path)
    app.mainloop()


if __name__ == "__main__":
    main()
