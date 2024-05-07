import customtkinter as ctk


class StatisticFrame(ctk.CTkFrame):
    def __init__(self, master, title, initial_value="0", title_font=18, val_font=24, **kwargs):
        super().__init__(master, **kwargs)
        self.title_label = ctk.CTkLabel(self, 
                                        text=title, 
                                        font=("Helvetica", title_font), anchor="n")

        self.value_var   =ctk.StringVar(value=initial_value)
        self.value_label = ctk.CTkLabel(self, 
                                        textvariable=self.value_var, 
                                        font=("Helvetica", val_font), anchor="center")

        self.pack(pady=(10, 15), fill="x")
        self.title_label.pack(fill="x")
        self.value_label.pack(pady=(5, 0), fill="x")

    def set_value(self, value):
        self.value_var.set(value)


class ButtonFrame(ctk.CTkFrame):
    def __init__(self, master, title, btntext, callback, **kwargs):
        super().__init__(master, **kwargs)
        self.label       = ctk.CTkLabel(self, 
                                        text=title, 
                                        font=("Helvetica", 18))
        self.button      =ctk.CTkButton(self, 
                                        text=btntext, 
                                        width=90, 
                                        font=("Roboto", 16), 
                                        command=callback)

        self.pack()
        self.label.pack(pady=(20, 8))
        self.button.pack()
