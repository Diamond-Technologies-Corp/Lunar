import json
import sys
from pathlib import Path

import customtkinter as ctk

BASE_DIR = (
    Path(sys.executable).parent
    if getattr(sys, "frozen", False)
    else Path(__file__).resolve().parent
)
CONFIG_PATH = BASE_DIR / "config.json"

DEFAULT_BORDER = "#565b5e"
GREY_TEXT = "#767474"
GREEN = "#23d34c"

state = {"step": "country"}


def load_config() -> dict:
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_config(data: dict) -> None:
    with open(CONFIG_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.title("Lunar - Setup | By Diamond Technologies")
root.geometry("1080x720")
root.minsize(480, 360)
root.grid_columnconfigure(0, weight=1)

label_title = ctk.CTkLabel(
    root,
    text="Welcome to Lunar!",
    font=("Open Sans", 40, "bold"),
    text_color="white",
)
label_title.grid(row=0, column=0, padx=20, pady=(40, 10))

entry = ctk.CTkEntry(root, placeholder_text="Country", width=300)
entry.grid(row=2, column=0, pady=(0, 10))

label_info = ctk.CTkLabel(
    root,
    text="We need your location to calculate prayer times (100% local).",
    font=("Open Sans", 20),
    text_color=GREY_TEXT,
    wraplength=600,
)
label_info.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")

btn_confirm = ctk.CTkButton(
    root,
    text="Confirm",
    fg_color=GREEN,
    text_color="white",
    corner_radius=5,
    cursor="hand2",
)
btn_confirm.grid(row=4, column=0)

label_warning = ctk.CTkLabel(root, text="", fg_color="red", text_color="white")


def show_error(message: str) -> None:
    label_warning.configure(text=message)
    label_warning.grid(row=5, column=0, pady=(15, 0))
    entry.configure(border_color="red")


def hide_error() -> None:
    label_warning.grid_forget()
    entry.configure(border_color=DEFAULT_BORDER)


def confirm(event=None) -> None:
    value = entry.get().strip()

    if not value:
        show_error("Error: The text field is empty!")
        return

    hide_error()

    data = load_config()
    if not isinstance(data.get("location"), dict):
        data["location"] = {}

    if state["step"] == "country":
        data["location"]["country"] = value
        try:
            save_config(data)
        except OSError:
            show_error("Error: Could not save your settings.")
            return

        state["step"] = "city"
        entry.delete(0, "end")
        entry.configure(placeholder_text="City")
        label_info.configure(text="Which city do you live in?")
        root.focus()

    else:
        data["location"]["city"] = value
        try:
            save_config(data)
        except OSError:
            show_error("Error: Could not save your settings.")
            return

        entry.configure(border_color=GREEN, state="disabled")
        btn_confirm.configure(state="disabled")
        label_info.configure(
            text="Perfect! Your location was saved successfully.",
            text_color=GREEN,
        )
        method()
        # root.after(1500, root.destroy)


btn_confirm.configure(command=confirm)
entry.bind("<Return>", confirm)
def method():
    for widget in root.winfo_children():
        widget.destroy()

    label_title = ctk.CTkLabel(
        root,
        text="Thx! Which calculation method do you want to use?",
        font=("Open Sans", 40, "bold"),
        text_color="white",
    )
    label_title.grid(row=0, column=0, padx=20, pady=(40, 10))

    values = [
        "Muslim World League (Fajr 18° / Isha 17°)",
        "ISNA (15° / 15°)",
        "Egyptian (19.5° / 17.5°)",
        "Karachi (18° / 18°)",
        "Umm al-Qura (18.5° / 90 min after Maghrib)",
        "UOIF (12° / 12°)",
        "Diyanet (18° / 17°)",
    ]


    method = ctk.CTkComboBox(
        root,
        values=values,
        border_color="green",
        width=300,
        font=("Open Sans", 12),
    )
    method.grid(row=1, column=0, pady=(0, 10))
    method.set(values[0])

    btn_confirm = ctk.CTkButton(
        root,
        text="Confirm",
        fg_color=GREEN,
        text_color="white",
        corner_radius=5,
        cursor="hand2",
    )
    btn_confirm.grid(row=4, column=0)

    label_advices = ctk.CTkLabel(
        root,
        text=(
    "UOIF: France\n"
    "Muslim World League: Europe and international\n"
    "Umm al-Qura: Saudi Arabia and the Gulf\n"
    "ISNA: North America\n"
    "Karachi: South Asia\n"
    "Diyanet: Turkey"
),
        text_color="white",
        cursor="hand2",
        wraplength=700,
        justify="left",
    )
    label_advices.grid(row=5, padx=20, pady=10, sticky="ew")

    label_version = ctk.CTkLabel(
        root, 
        text="Version: 1.1",
        text_color="white",
    )
    label_version.grid(row=6)


root.mainloop()