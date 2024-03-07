import customtkinter as ctk
from datetime import datetime
from src.utils import load_data


class StatsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.data_file = 'data.json'

        self.total_today_var = ctk.StringVar(value="Pomodoros Today:  0")
        self.total_today = ctk.CTkLabel(self, textvariable=self.total_today_var, font=("Helvetica", 16, "bold"), anchor="w")
        self.total_today.pack(padx=20, pady=(20, 0), fill="x")

        self.total_hours_var = ctk.StringVar(value="Total Hours Studied:  0")
        self.total_hours = ctk.CTkLabel(self, textvariable=self.total_hours_var, font=("Helvetica", 16, "bold"), anchor="w")
        self.total_hours.pack(padx=20, pady=(20, 0), fill="x")

        self.total_var = ctk.StringVar(value="Total Pomodoros:  0")
        self.total = ctk.CTkLabel(self, textvariable=self.total_var, font=("Helvetica", 16, "bold"), anchor="w")
        self.total.pack(padx=20, pady=(20, 0), fill="x")

        self.update_stats = ctk.CTkButton(self, text="Update", width=90, font=("Roboto", 16), command=self.load_stats)
        self.update_stats.pack(pady=40, side=ctk.BOTTOM)

        self.load_stats()

    def load_stats(self):
        data = load_data()
        if not data:
            return

        current_date = datetime.now().strftime("%Y-%m-%d")
        total_today = data.get('sessions_by_date', {}).get(current_date, 0)

        self.total_today_var.set(f"Pomodoros Today:  {total_today}")

        total_seconds_studied = data.get('total_seconds_studied', 0)
        total_hours = total_seconds_studied / 3600

        self.total_hours_var.set(f"Total Hours Studied:  {total_hours:.1f}")

        self.total_var.set(f"Total Pomodoros:  {data.get('total_pomodoro_sessions', 0)}")

