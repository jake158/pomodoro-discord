import pypresence

CLIENT_ID = '1215345125002059836'


class RichPresence(pypresence.Presence):
    def __init__(self):
        super().__init__(client_id=CLIENT_ID)
        # Can only update every 15 seconds
        try:
            self.connect()
            self.default_state()
        except Exception as e:
            print(f"Failed to connect to Discord: {e}")

    def default_state(self):
        self.update(state="Idling", details=None, large_image="graytomato",
                    large_text="github.com/freeram/pomodoro-discord")

    def running_state(self, session, start_time, end_time):
        self.update(state=f"Session {session}", details="Studying", start=start_time,
                    end=end_time, large_image="tomato", large_text="github.com/freeram/pomodoro-discord")

    def break_state(self, complete, start_time, end_time):
        self.update(state=f"On break. Sessions completed: {complete}", details=None, start=start_time,
                    end=end_time, large_image="greentomato", large_text="github.com/freeram/pomodoro-discord")
