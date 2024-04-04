import customtkinter as ctk
from datetime import datetime
from src.components.statistic_display import StatisticDisplay
from src.utils import load_data
from src.logic.graphs import graph_pomodoro_sessions, graph_hours_studied


class StatsFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.time_today = StatisticDisplay(self, "Time Studied Today:")
        self.pomodoros_today = StatisticDisplay(self, "Pomodoros Today:")
        self.total_hours = StatisticDisplay(self, "Total Time Studied:")
        self.total_pomodoros = StatisticDisplay(self, "Total Pomodoros:")
        
        self.update_stats = ctk.CTkButton(self, text="Update", width=90, font=("Roboto", 16), command=self.load_stats)
        self.update_stats.pack(pady=(10, 0))
        
        self.graph_label_1 = ctk.CTkLabel(self, text="Pomodoro Sessions Graph", font=("Helvetica", 18))
        self.graph_label_1.pack(pady=(32, 8))
        self.graph_button_1 = ctk.CTkButton(self, text="Show", width=90, font=("Roboto", 16), command=self.show_sessions_graph)
        self.graph_button_1.pack()
        
        self.graph_label_2 = ctk.CTkLabel(self, text="Hours Studied Graph", font=("Helvetica", 18))
        self.graph_label_2.pack(pady=(20, 8))
        self.graph_button_2 = ctk.CTkButton(self, text="Show", width=90, font=("Roboto", 16), command=self.show_hours_graph)
        self.graph_button_2.pack()
        
        self.load_stats()
    
    def load_stats(self):
        data = load_data()
        if not data:
            return
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        total_today_seconds = data.get('seconds_by_date', {}).get(current_date, 0)
        total_today_hours = total_today_seconds / 3600
        if total_today_hours < 1:
            self.time_today.set_value(f"{total_today_seconds // 60} minute{'s' if total_today_seconds // 60 != 1 else ''}")
        else:
            self.time_today.set_value(f"{total_today_hours:.1f} hours")
        
        total_today_pomodoros = data.get('sessions_by_date', {}).get(current_date, 0)
        self.pomodoros_today.set_value(f"{total_today_pomodoros} session{'s' if total_today_pomodoros != 1 else ''}")
        
        total_seconds = data.get('total_seconds_studied', 0)
        total_hours = data.get('total_seconds_studied', 0) / 3600
        if total_hours < 1:
            self.total_hours.set_value(f"{total_seconds // 60} minute{'s' if total_seconds // 60 != 1 else ''}")
        else:
            self.total_hours.set_value(f"{total_hours:.1f} hours")
        
        total_pomodoros = data.get('total_pomodoro_sessions', 0)
        self.total_pomodoros.set_value(f"{total_pomodoros} session{'s' if total_pomodoros != 1 else ''}")
    
    def show_sessions_graph(self):
        graph_pomodoro_sessions(load_data())
    
    def show_hours_graph(self):
        graph_hours_studied(load_data())
