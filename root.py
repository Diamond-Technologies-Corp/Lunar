import customtkinter as ctk
from update import apply_update, check_for_updates, launch
import bg

ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.title("Lunar")
root.geometry("1000x520")
root.minsize(780, 460)
root.grid_columnconfigure(0, weight=1)

label_title = ctk.CTkLabel(root, text="Lunar", font=("Open Sans", 30))
label_title.grid(row=1, pady=20)



def show_background():
  background = ctk.CTkImage





def updating():
  print("Starting Verification...")
  result = check_for_updates()

  if result["update_available"]:
    print(
        f"New version available : {result['latest_version']} (Today"
        f" : {result['current_version']})"
    )

    label_important = ctk.CTkLabel(
        root,
        text=(
            "Hi! Sorry to interrupt you, but... a new version of Lunar is"
            " actually available."
        ),
        font=("Open Sans", 15),
    )
    label_important.grid(row=2, pady=10)

    buttons_frame = ctk.CTkFrame(root, fg_color="transparent")
    buttons_frame.grid(row=3, column=0, columnspan=2, pady=10)

    def Yes():
      print("You said Yes")
      zip_path = launch()
      if zip_path:
        apply_update(zip_path)
      else:
        print("[Error] Impossible d'appliquer la mise à jour (zip introuvable).")

    install_btn = ctk.CTkButton(
        buttons_frame,
        text="Install it!",
        fg_color="#2E8B57",
        text_color="white",
        corner_radius=5,
        cursor="hand2",
        command=Yes,
    )
    install_btn.pack(side="left", padx=5)

    def No():
      print("You said No")
      for widget in root.winfo_children():
        if widget not in [label_title]:
          widget.destroy()

    no_btn = ctk.CTkButton(
        buttons_frame,
        text="Nahh, not now (do ctrl + i to install).",
        fg_color="#333333",
        text_color="white",
        corner_radius=5,
        cursor="hand2",
        command=No,
    )
    no_btn.pack(side="left", padx=5)
  else:
    print("Lunar is already up to date.")


root.after(500, updating)

root.mainloop()