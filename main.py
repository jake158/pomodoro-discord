import customtkinter as ctk

MAIN_RED = "#eb4034"
RED_HOVER = "#f75a4f"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class PomodoroFrame(ctk.CTkFrame):
    def __init__(self, master, start_func):
        super().__init__(master)

        # Placeholder
        self.timer_display = ctk.CTkLabel(self, text="00:25:00", font=("Helvetica", 48))
        self.timer_display.pack(pady=50)

        self.start_button = ctk.CTkButton(self, text="Start", fg_color="transparent", border_color=MAIN_RED,
                                          border_width=2, corner_radius=32, hover_color=RED_HOVER, command=start_func)
        self.start_button.pack()


class PomodoroApp(ctk.CTk):
    WIDTH = 400
    HEIGHT = 400

    def __init__(self):
        super().__init__()

        self.title("Pomodoro Tracker")
        self.geometry(f"{PomodoroApp.WIDTH}x{PomodoroApp.HEIGHT}")

        tabview = ctk.CTkTabview(master=self)
        tabview.pack(padx=20, pady=20)

        tabview.add("Main")
        tabview.add("Settings")

        self.main_frame = PomodoroFrame(tabview.tab("Main"), self.start_timer)
        self.main_frame.pack()

    def start_timer(self):
        print("Timer started")


if __name__ == "__main__":
    app = PomodoroApp()
    app.mainloop()
