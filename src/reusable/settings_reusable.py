import customtkinter as ctk


class EntryFrame(ctk.CTkFrame):
    def __init__(self, master, text, config, config_attr, defvalue, command):
        super().__init__(master)
        self.label          = ctk.CTkLabel(self, 
                                           text=text)
        
        self.controls_frame = ctk.CTkFrame(self)
        
        self.entry_var      =   ctk.IntVar(value=config.get(config_attr, defvalue))
        self.entry          = ctk.CTkEntry(self.controls_frame, 
                                           width=35, 
                                           textvariable=self.entry_var)
        
        self.set_button     =ctk.CTkButton(self.controls_frame, 
                                           width=120, 
                                           text="Set", 
                                           command=command)

        self.pack(pady=(5, 0))
        self.label.pack(pady=(10, 10), padx=(10, 10))
        self.controls_frame.pack(fill=ctk.X, expand=True, padx=10)
        self.entry.pack(side=ctk.LEFT, fill=ctk.X, expand=True, padx=(0, 10))
        self.set_button.pack(side=ctk.RIGHT)
    
    def get(self):
        return self.entry_var.get()
