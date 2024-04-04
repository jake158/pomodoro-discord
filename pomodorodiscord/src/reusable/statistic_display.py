import customtkinter as ctk


class StatisticDisplay(ctk.CTkFrame):
    def __init__(self, master, title, initial_value="0", title_font=18, val_font=24, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(pady=(10, 15), fill="x")
        
        self.title_label = ctk.CTkLabel(self, text=title, font=("Helvetica", title_font), anchor="n")
        self.title_label.pack(fill="x")
        
        self.value_var = ctk.StringVar(value=initial_value)
        self.value_label = ctk.CTkLabel(self, textvariable=self.value_var, font=("Helvetica", val_font), anchor="center")
        self.value_label.pack(pady=(5, 0), fill="x")
    
    def set_value(self, value):
        self.value_var.set(value)
