import os
import customtkinter as ctk
from src.utils import load_config, save_config, reload_app, DEF_POMODORO_MINS, DEF_SB_MINS, DEF_LB_MINS, DEF_SB_BEFORE_L, beep


class EntryFrame(ctk.CTkFrame):
    def __init__(self, master, text, config, config_attr, defvalue, command):
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

        # Automatic Break Cycling
        self.abcycling_var = ctk.IntVar(value=config.get("auto_break_cycling", 0))
        self.abcycling_switch = ctk.CTkCheckBox(self, text=" Automatic break cycling", border_width=2, variable=self.abcycling_var, onvalue=1, offvalue=0, command=self.change_abcycling)
        self.abcycling_switch.pack(pady=(10, 0))

        # Short Breaks Before Long Break
        self.sb_before_l_entry = EntryFrame(self, "Short breaks before\nlong break (if auto cycling):", config, "short_breaks_before_long", DEF_SB_BEFORE_L, self.change_sb_before_l)
        self.sb_before_l_entry.pack(pady=(10, 0))

        # Pomodoro Duration
        self.pomodoro_entry = EntryFrame(self, "Pomodoro Duration (mins):", config, "pomodoro_time", DEF_POMODORO_MINS, self.change_pomodoro_time)
        self.pomodoro_entry.pack(pady=(5, 0))

        # Short Break Duration
        self.sb_entry = EntryFrame(self, "Short Break Duration (mins):", config, "short_break_time", DEF_SB_MINS, self.change_sb_time)
        self.sb_entry.pack(pady=(5, 0))

        # Long Break Duration
        self.lb_entry = EntryFrame(self, "Long Break Duration (mins):", config, "long_break_time", DEF_LB_MINS, self.change_lb_time)
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

    def change_abcycling(self):
        config = load_config()
        config["auto_break_cycling"] = self.abcycling_var.get()
        save_config(config)

    def change_time(self, entry, config_param):
        time = entry.get()
        if time and time > 0:
            config = load_config()
            config[config_param] = time
            save_config(config)

    def change_sb_before_l(self):
        self.change_time(self.sb_before_l_entry, "short_breaks_before_long")

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
        config['volume'] = int(volume * 100)
        save_config(config)
