import customtkinter as ctk
import json

ctk.set_appearance_mode("dark")

root = ctk.CTk()

root.title("Lunar - Setup | By Diamond Technologies")
root.geometry("1080x720")
root.minsize(480, 360)

label_title = ctk.CTkLabel(root, text="Welcome in Lunar!", font=("Open Sans",40, "bold"), text_color="white")
label_title.grid(
    row=0, 
    column=0, 
    padx=20,         
    pady=(40, 10)    
)

entry = ctk.CTkEntry(root, placeholder_text="Country")
entry.grid(row=2)

label_info = ctk.CTkLabel(root, text="We need your location to calculate prayer times (100% local).", font=("Open Sans", 20), text_color="#767474")
label_info.grid(row=3, column=0, padx=20, pady=(0,20), sticky="ew")
root.grid_columnconfigure(0, weight=1)

def confirm():
    result = entry.get().strip()

    if not result: 
        label_warning = ctk.CTkLabel(root, text="Error: The text field is empty!", fg_color="red")
        label_warning.grid(row=5)
        entry.configure(border_color="red")




btn_confirm = ctk.CTkButton(root, text="Confirm", fg_color="#23d34c", text_color="white", corner_radius=5, cursor="hand2", command=confirm)
btn_confirm.grid(row=4)

def save_locations():
    print("Hello World")


root.mainloop()