import customtkinter as ctk


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("themes/Default.json")


class PomodoroFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.timer_display = ctk.CTkLabel(self, text="25:00", font=("Helvetica", 58))
        self.timer_display.pack(pady=50)

        self.start_button = ctk.CTkButton(self, text="Start", fg_color="transparent",
                                          border_width=2, corner_radius=32, command=self.start_timer)
        self.start_button.pack()

    def start_timer(self):
        print("Timer started")


class TabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.add("Main")
        self.add("Settings")

        self.main_frame = PomodoroFrame(self.tab("Main"))
        self.main_frame.pack()


class PomodoroApp(ctk.CTk):
    WIDTH = 350
    HEIGHT = 350

    def __init__(self):
        super().__init__()

        self.title("Pomodoro Tracker")
        self.geometry(f"{PomodoroApp.WIDTH}x{PomodoroApp.HEIGHT}")

        self.tabview = TabView(master=self)
        self.tabview.pack(pady=30)


if __name__ == "__main__":
    app = PomodoroApp()
    app.mainloop()
