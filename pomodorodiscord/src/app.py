import customtkinter as ctk
from src.frames.pomodoro_frame import PomodoroFrame
from src.frames.settings_frame import SettingsFrame
from src.frames.stats_frame import StatsFrame


class TabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, command=self.on_tab_change)
        self.add("Main")
        self.add("Settings")
        self.add("Stats")

        self.main_frame = PomodoroFrame(self.tab("Main"))
        self.main_frame.pack(expand=True, fill='both')

        self.settings_frame = SettingsFrame(self.tab("Settings"))
        self.settings_frame.pack(expand=True, fill='both')

        self.stats_frame = StatsFrame(self.tab("Stats"))
        self.stats_frame.pack(expand=True, fill='both')

        # Fixing scrolling on Linux
        # https://github.com/TomSchimansky/CustomTkinter/issues/1356
        self.stats_frame.bind_all("<Button-4>", lambda e: [frame._parent_canvas.yview("scroll", -1, "units") for frame in (self.stats_frame, self.settings_frame)])
        self.stats_frame.bind_all("<Button-5>", lambda e: [frame._parent_canvas.yview("scroll", 1, "units") for frame in (self.stats_frame, self.settings_frame)])

    def on_tab_change(self):
        if self.get() == "Stats":
            self.stats_frame.load_stats()


class PomodoroApp(ctk.CTk):
    WIDTH = 350
    HEIGHT = 400

    def __init__(self):
        super().__init__()
        self.title("Pomodoro Tracker")
        self.geometry(f"{PomodoroApp.WIDTH}x{PomodoroApp.HEIGHT}")

        self.tabview = TabView(master=self)
        self.tabview.pack(pady=(15, 30), expand=True, fill='y')
