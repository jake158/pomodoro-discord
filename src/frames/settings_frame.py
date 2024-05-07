import os
import customtkinter as ctk
from src.reusable.settings_reusable import EntryFrame
from src.utils import THEMES_DIR, load_config, save_config, reload_app, beep, DEF_POMODORO_MINS, DEF_SB_MINS, DEF_LB_MINS, DEF_SB_BEFORE_L


class SettingsFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        config = load_config()
        self.initialize_ui(config)

    def initialize_ui(self, config):
        # ABC
        self.abcycling_var   =       ctk.IntVar(value=config.get("auto_break_cycling", 0))
        self.abcycling_switch=  ctk.CTkCheckBox(self,
                                                text=" Automatic break cycling", 
                                                border_width=2, 
                                                variable=self.abcycling_var, 
                                                onvalue=1, 
                                                offvalue=0, 
                                                command=self.change_abcycling)
        self.abcycling_switch.pack(pady=(10, 5))
        
        # Enter a number frames
        self.sbl_entry       =       EntryFrame(self, 
                                                text="Short breaks before\nlong break (if auto cycling):", 
                                                config=config, 
                                                config_attr="short_breaks_before_long", 
                                                defvalue=DEF_SB_BEFORE_L, 
                                                command=self.change_sb_before_l)
        self.pomodoro_entry  =       EntryFrame(self, 
                                                text="Pomodoro Duration (mins):", 
                                                config=config, 
                                                config_attr="pomodoro_time", 
                                                defvalue=DEF_POMODORO_MINS, 
                                                command=self.change_pomodoro_time)
        self.sb_entry        =       EntryFrame(self, 
                                                text="Short Break Duration (mins):", 
                                                config=config, 
                                                config_attr="short_break_time", 
                                                defvalue=DEF_SB_MINS, 
                                                command=self.change_sb_time)
        self.lb_entry        =       EntryFrame(self, 
                                                text="Long Break Duration (mins):", 
                                                config=config, 
                                                config_attr="long_break_time", 
                                                defvalue=DEF_LB_MINS, 
                                                command=self.change_lb_time)
        
        # Theme selection
        self.theme_label     =     ctk.CTkLabel(self, 
                                                text="Select Theme (RESTARTS APP):")

        self.theme_options   = [os.path.splitext(theme)[0] for theme in os.listdir(THEMES_DIR) if theme.endswith('.json')]
        selected             = ctk.StringVar(value=config.get('theme', 'Default'))

        self.theme_menu      =ctk.CTkOptionMenu(self, 
                                                variable=selected, 
                                                values=self.theme_options, 
                                                anchor="n", 
                                                command=self.change_theme)

        # Volume controls
        self.volume_label =        ctk.CTkLabel(self, 
                                                text="Adjust Beep Volume:")
        self.volume_slider =      ctk.CTkSlider(self, 
                                                from_=0, 
                                                to=100, 
                                                number_of_steps=100, 
                                                command=self.change_volume)
        self.volume_slider.set(config.get('volume', 10))
        self.change_volume(config.get('volume', 10))
        
        self.beep_button =        ctk.CTkButton(self, 
                                                text="Play", 
                                                width=70, 
                                                command=beep.play)
        
        self.theme_label.pack(pady=(20, 0))
        self.theme_menu.pack(pady=(10, 0))
        self.volume_label.pack(pady=(20, 0))
        self.volume_slider.pack(pady=(10, 0))
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
        self.change_time(self.sbl_entry, "short_breaks_before_long")

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
