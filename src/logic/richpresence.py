import pypresence
from datetime import datetime
from src.utils import load_data

CLIENT_ID = '1215345125002059836'


class RichPresence(pypresence.Presence):
    def __init__(self):
        super().__init__(client_id=CLIENT_ID)
        self.launch_time = datetime.now().timestamp()
        # Can only update every 15 seconds
        self.connected = False
        self.connect()
        self.total_seconds_studied = load_data().get('total_seconds_studied', 0)
        self.idling_state()

    def _handle_exceptions(func):
        def wrapper(self, *args, **kwargs):
            if not self.connected:
                return
            try:
                func(self, *args, **kwargs)
            except Exception as e:
                print(f"Error updating Rich Presence: {e}")
                self.connected = False
        return wrapper

    def connect(self):
        try:
            super().connect()
            self.connected = True
            return True
        except Exception as e:
            print(f"Failed to connect to Discord: {e}")
            self.connected = False
            return False

    def disconnect(self):
        try:
            super().close()
            self.connected = False
            return True
        except Exception as e:
            print(f"Failed to disconnect from Discord: {e}")
            self.connected = True
            return False

    def format_time(self, seconds_studied):
        total_seconds = seconds_studied
        total_hours = seconds_studied / 3600
        if total_hours < 1:
            return f"{total_seconds // 60} minute{'s' if total_seconds // 60 != 1 else ''}"
        else:
            return f"{round(total_hours, 1) if total_hours % 1 != 0 else int(total_hours)} hours"

    @_handle_exceptions
    def idling_state(self, seconds_studied=0):
        self.update(state=f"Total time studied: {self.format_time(self.total_seconds_studied + seconds_studied)}", 
                    details="Idling", start=self.launch_time, large_image="graytomato", large_text="github.com/freeram/pomodoro-discord")

    @_handle_exceptions
    def running_state(self, session, start_time, end_time):
        self.update(state=f"Session {session}", details="Studying", start=start_time,
                    end=end_time, large_image="tomato", large_text="github.com/freeram/pomodoro-discord")

    @_handle_exceptions
    def paused_state(self, start_time):
        self.update(state="Paused", details=None, start=start_time, large_image="graytomato",
                    large_text="github.com/freeram/pomodoro-discord")

    @_handle_exceptions
    def break_state(self, seconds_studied, start_time, end_time):
        self.update(state=f"Time studied: {self.format_time(seconds_studied)}", details="On break", start=start_time,
                    end=end_time, large_image="greentomato", large_text="github.com/freeram/pomodoro-discord")
