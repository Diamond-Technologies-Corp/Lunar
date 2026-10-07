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

GREEN = "#23d34c"


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


def method():
    for widget in root.winfo_children():
        widget.destroy()

    label_title = ctk.CTkLabel(
        root,
        text="Which calculation method do you want to use?",
        font=("Open Sans", 40, "bold"),
        text_color="white",
        wraplength=900,
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

    method_selector = ctk.CTkComboBox(
        root,
        values=values,
        border_color="green",
        width=300,
        font=("Open Sans", 12),
        state="readonly",
    )
    method_selector.grid(row=1, column=0, pady=(0, 10))
    method_selector.set(values[0])

    method_feedback = ctk.CTkLabel(root, text="", text_color="white")
    method_feedback.grid(row=4, column=0, pady=(10, 0))

    def confirm_method() -> None:
        selected_method = method_selector.get()
        if selected_method not in values:
            method_feedback.configure(
                text="Error: Please select a calculation method.",
                text_color="red",
            )
            return

        data = load_config()
        if not isinstance(data.get("location"), dict):
            data["location"] = {}
        data["location"]["method"] = selected_method

        try:
            save_config(data)
        except OSError:
            method_feedback.configure(
                text="Error: Could not save your settings.",
                text_color="red",
            )
            return

        method_feedback.configure(text="Please wait...", text_color=GREEN)
        root.after(2000, finish)

    btn_confirm = ctk.CTkButton(
        root,
        text="Confirm",
        fg_color=GREEN,
        text_color="white",
        corner_radius=5,
        cursor="hand2",
        command=confirm_method,
    )
    btn_confirm.grid(row=3, column=0)

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
        wraplength=700,
        justify="left",
    )
    label_advices.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

    label_version = ctk.CTkLabel(root, text="Version: 1.1", text_color="white")
    label_version.grid(row=6, column=0)


def finish():
    # La boucle ne fait que détruire : tout le reste est en dehors.
    for widget in root.winfo_children():
        widget.destroy()

    progressbar = ctk.CTkProgressBar(
        root,
        orientation="horizontal",
        progress_color="pink",
        mode="indeterminate",
        indeterminate_speed=0.5,
    )
    progressbar.grid(row=1, column=0, pady=(40, 10))
    progressbar.start()

    label_info = ctk.CTkLabel(
        root,
        text="Last ask: What are the coordinates of your city?",
        text_color="white",
        font=("Open Sans", 20),
    )
    label_info.grid(row=2, column=0)

    label_advices = ctk.CTkLabel(
        root,
        text="Advice: search on the Internet 'coordinates x', x = name of your city (decimal format).",
        text_color="white",
    )
    label_advices.grid(row=3, column=0, pady=(0, 10))

    latitude_entry = ctk.CTkEntry(
        root, placeholder_text="Latitude in decimal format.", width=200
    )
    longitude_entry = ctk.CTkEntry(
        root, placeholder_text="Longitude in decimal format.", width=200
    )
    latitude_entry.grid(row=5, column=0, pady=(0, 10))
    longitude_entry.grid(row=6, column=0, pady=(0, 10))

    feedback = ctk.CTkLabel(root, text="", text_color="white")
    feedback.grid(row=8, column=0, pady=(10, 0))

    def lg() -> None:
        try:
            lat_val = float(latitude_entry.get().strip().replace(",", "."))
            longitude_val = float(longitude_entry.get().strip().replace(",", "."))
        except ValueError:
            feedback.configure(text="Error: Please enter valid numbers.", text_color="red")
            return

        if not (-90 <= lat_val <= 90 and -180 <= longitude_val <= 180):
            feedback.configure(
                text="Error: Latitude must be between -90 and 90, longitude between -180 and 180.",
                text_color="red",
            )
            return

        data = load_config()
        if not isinstance(data.get("location"), dict):
            data["location"] = {}
        data["location"]["latitude"] = lat_val
        data["location"]["longitude"] = longitude_val
        data["did_setup"] = True

        try:
            save_config(data)
        except OSError:
            feedback.configure(text="Error: Could not save your settings.", text_color="red")
            return

        feedback.configure(text="Perfect! Your location was saved successfully.", text_color=GREEN)
        btn_confirm.configure(state="disabled")
        root.after(1500, root.destroy)

    btn_confirm = ctk.CTkButton(
        root,
        text="Confirm",
        fg_color=GREEN,
        text_color="white",
        corner_radius=5,
        cursor="hand2",
        command=lg,
    )
    btn_confirm.grid(row=9, column=0)


method()
root.mainloop()