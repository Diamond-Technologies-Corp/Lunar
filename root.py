import customtkinter as ctk
import json 

ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.title("Lunar ")
root.geometry("1000x520")
root.minsize(780, 460)
root.grid_columnconfigure(0, weight=1)

label_title = ctk.CTkLabel(
    root,
    text="Lunar",
    font=("Open Sans", 30)
)
label_title.grid(row=1)


root.mainloop()