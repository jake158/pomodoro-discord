# Can only update every 15 seconds
import pypresence

CLIENT_ID = '1215345125002059836'


class RichPresence(pypresence.Presence):
    def __init__(self):
        super().__init__(client_id=CLIENT_ID)
        try:
            self.connect()
            self.default_state()
        except Exception as e:
            print(f"Failed to connect to Discord: {e}")

    def default_state(self):
        self.update(state="Placeholder",
                    details="Placeholder details", large_image="tomato")

    def begin_pomodoro(self):
        pass

    def begin_break(self):
        pass
