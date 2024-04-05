import pypresence
from datetime import datetime

CLIENT_ID = '1215345125002059836'


class RichPresence(pypresence.Presence):
    def __init__(self):
        super().__init__(client_id=CLIENT_ID)
        self.launch_time = datetime.now().timestamp()
        # Can only update every 15 seconds
        try:
            self.connect()
            self.default_state()
        except Exception as e:
            print(f"Failed to connect to Discord: {e}")

    def format_time(self, seconds_studied):
        total_seconds = seconds_studied
        total_hours = seconds_studied / 3600

        if total_hours < 1:
            return f"{total_seconds // 60} minute{'s' if total_seconds // 60 != 1 else ''}"
        else:
            return f"{total_hours:.1f} hours"

    def default_state(self):
        self.update(state="Idling", details=None, start=self.launch_time, large_image="graytomato",
                    large_text="github.com/freeram/pomodoro-discord")

    def running_state(self, session, start_time, end_time):
        self.update(state=f"Session {session}", details="Studying", start=start_time,
                    end=end_time, large_image="tomato", large_text="github.com/freeram/pomodoro-discord")

    def break_state(self, seconds_studied, start_time, end_time):
        self.update(state=f"Time studied: {self.format_time(seconds_studied)}", details="On break", start=start_time,
                    end=end_time, large_image="greentomato", large_text="github.com/freeram/pomodoro-discord")
