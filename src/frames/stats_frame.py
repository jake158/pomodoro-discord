import customtkinter as ctk
from datetime import datetime
from CTkMessagebox import CTkMessagebox
from src.reusable.stats_reusable import StatisticFrame, ButtonFrame
from src.utils import load_data
from src.logic.graphs import graph_pomodoro_sessions, graph_hours_studied


class StatsFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.time_today = StatisticFrame(self, "Time Studied Today:")
        self.pomodoros_today = StatisticFrame(self, "Pomodoros Today:")
        self.total_hours = StatisticFrame(self, "Total Time Studied:")
        self.total_pomodoros = StatisticFrame(self, "Total Pomodoros:")
        self.graph_btn_1 = ButtonFrame(self, "Pomodoro Sessions Graph", "Show", self.show_sessions_graph)
        self.graph_btn_2 = ButtonFrame(self, "Hours Studied Graph", "Show", self.show_hours_graph)
        self.load_stats()

    def load_stats(self):
        data = load_data()
        if not data:
            return

        current_date = datetime.now().strftime("%Y-%m-%d")
        self.update_time_today(data, current_date)
        self.update_pomodoros_today(data, current_date)
        self.update_total_hours(data)
        self.update_total_pomodoros(data)

    def update_time_today(self, data, current_date):
        total_today_seconds = data.get('seconds_by_date', {}).get(current_date, 0)
        total_today_hours = total_today_seconds / 3600
        if total_today_hours < 1:
            self.time_today.set_value(f"{total_today_seconds // 60} minute{'s' if total_today_seconds // 60 != 1 else ''}")
        else:
            self.time_today.set_value(f"{total_today_hours:.1f} hours")

    def update_pomodoros_today(self, data, current_date):
        total_today_pomodoros = data.get('sessions_by_date', {}).get(current_date, 0)
        self.pomodoros_today.set_value(f"{total_today_pomodoros} session{'s' if total_today_pomodoros != 1 else ''}")

    def update_total_hours(self, data):
        total_seconds = data.get('total_seconds_studied', 0)
        total_hours = total_seconds / 3600
        if total_hours < 1:
            self.total_hours.set_value(f"{total_seconds // 60} minute{'s' if total_seconds // 60 != 1 else ''}")
        else:
            self.total_hours.set_value(f"{total_hours:.1f} hours")

    def update_total_pomodoros(self, data):
        total_pomodoros = data.get('total_pomodoro_sessions', 0)
        self.total_pomodoros.set_value(f"{total_pomodoros} session{'s' if total_pomodoros != 1 else ''}")

    def _ensure_exists(self, param, msg):
        data = load_data()
        value = data.get(param, 0)
        if value == 0:
            CTkMessagebox(title="Error", message=msg, icon="cancel")
            return False
        return True

    def show_sessions_graph(self):
        if not self._ensure_exists('total_pomodoro_sessions', 'Cannot graph pomodoro sessions: none recorded'):
            return
        graph_pomodoro_sessions(load_data())

    def show_hours_graph(self):
        if not self._ensure_exists('total_seconds_studied', 'Cannot graph hours studied: none recorded'):
            return
        graph_hours_studied(load_data())
