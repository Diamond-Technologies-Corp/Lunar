import json
import sys
from pathlib import Path

import customtkinter as ctk

from computation import METHODS, run_computation

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


def clear_window() -> None:
    for widget in root.winfo_children():
        widget.destroy()


ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.title("Lunar - Setup | By Diamond Technologies")
root.geometry("1000x520")
root.minsize(780, 460)
root.grid_columnconfigure(0, weight=1)


# ---------------------------------------------------------------- Étape 1
def method() -> None:
    clear_window()

    label_title = ctk.CTkLabel(
        root,
        text="Which calculation method do you want to use?",
        font=("Open Sans", 40, "bold"),
        text_color="white",
        wraplength=900,
    )
    label_title.grid(row=0, column=0, padx=20, pady=(40, 10))

    # Source unique : les clés de METHODS (computation.py)
    values = list(METHODS.keys())

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
        if selected_method not in METHODS:
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

        btn_method.configure(state="disabled")
        method_feedback.configure(text="Please wait...", text_color=GREEN)
        root.after(1000, coordinates)

    btn_method = ctk.CTkButton(
        root,
        text="Confirm",
        fg_color=GREEN,
        text_color="white",
        corner_radius=5,
        cursor="hand2",
        command=confirm_method,
    )
    btn_method.grid(row=3, column=0)

    label_advices = ctk.CTkLabel(
        root,
        text=(
            "UOIF: France\n"
            "Muslim World League: Europe and international\n"
            "Umm al-Qura: Saudi Arabia and the Gulf\n"
            "ISNA: North America\n"
            "Karachi: South Asia\n"
            "Egyptian: Africa and the Middle East\n"
        ),
        text_color="white",
        wraplength=700,
        justify="left",
    )
    label_advices.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

    label_version = ctk.CTkLabel(root, text="Version: 1.1", text_color="white")
    label_version.grid(row=6, column=0)


# ---------------------------------------------------------------- Étape 2
def coordinates() -> None:
    clear_window()

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
        text="What are the coordinates of your city?",
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
        # 1. Validation
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

        # 2. Sauvegarde de la localisation AVANT le calcul
        data = load_config()
        if not isinstance(data.get("location"), dict):
            data["location"] = {}
        data["location"]["latitude"] = lat_val
        data["location"]["longitude"] = longitude_val

        try:
            save_config(data)
        except OSError:
            feedback.configure(text="Error: Could not save your settings.", text_color="red")
            return

        # 3. Bouton désactivé + message d'attente
        btn_coords.configure(state="disabled")
        feedback.configure(text="Please wait...", text_color="white")
        root.update()

        # 4. Calcul des horaires (relit et réécrit config.json)
        try:
            run_computation()
        except Exception as e:
            feedback.configure(text=f"Error: {e}", text_color="red")
            btn_coords.configure(state="normal")
            return

        # 5. Setup marqué terminé seulement si le calcul a réussi
        try:
            data = load_config()
            data["did_setup"] = True
            save_config(data)
        except OSError:
            feedback.configure(text="Error: Could not save your settings.", text_color="red")
            btn_coords.configure(state="normal")
            return

        feedback.configure(
            text="Perfect! Your location was saved successfully.",
            text_color=GREEN,
        )
        root.after(1500, root.destroy)

    btn_coords = ctk.CTkButton(
        root,
        text="Confirm",
        fg_color=GREEN,
        text_color="white",
        corner_radius=5,
        cursor="hand2",
        command=lg,
    )
    btn_coords.grid(row=9, column=0)


# ---------------------------------------------------------------- Écran d'accueil
label_title = ctk.CTkLabel(
    root,
    text="Welcome in Lunar!",
    font=("Open Sans", 30),
)
label_title.grid(row=1)

btn_start = ctk.CTkButton(
    root,
    text="Start",
    fg_color=GREEN,
    text_color="white",
    corner_radius=5,
    cursor="hand2",
    command=method,
    font=("Open Sans", 17),
)
btn_start.grid(row=3, column=0)

root.mainloop()