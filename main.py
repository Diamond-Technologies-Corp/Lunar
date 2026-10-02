import importlib
import customtkinter as ctk
import root  # 

root = ctk.CTk()
root.geometry("600x400")
root.grid_columnconfigure(0, weight=1)

def reload_ui(event=None):
    importlib.reload(root)  # Recharge le fichier ui.py à chaud
    root.build_ui(root)     # Redessine l'interface
    print("UI Rechargée ! ⚡")


root.build_ui(root)

# Raccourci F5 ou Ctrl+R pour recharger sans fermer la fenêtre
root.bind("<F5>", reload_ui)
root.bind("<Control-r>", reload_ui)

root.mainloop()