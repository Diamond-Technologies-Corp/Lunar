import json
import sys
from pathlib import Path

import customtkinter as ctk
import subprocess
import sys
import threading
import time

from computation import METHODS, run_computation

BASE_DIR = (
    Path(sys.executable).parent
    if getattr(sys, "frozen", False)
    else Path(__file__).resolve().parent
)
CONFIG_PATH = BASE_DIR / "config.json"

GREEN = "#23d34c"

LANGUAGES = [
    "English",
    "French",
    "Spanish",
    "Italiano",
]


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
        text="Confirma",
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

    label_version = ctk.CTkLabel(root, text="Version: 1.2", text_color="white")
    label_version.grid(row=6, column=0)



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
        font=("Open Sans", 20, "bold"),
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

    def confirm_coordinates() -> None:
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

        try:
            save_config(data)
        except OSError:
            feedback.configure(text="Error: Could not save your settings.", text_color="red")
            return

        btn_coords.configure(state="disabled")
        feedback.configure(text="Please wait...", text_color=GREEN)

        root.after(500, last)

    btn_coords = ctk.CTkButton(
        root,
        text="Confirmo",
        fg_color=GREEN,
        text_color="white",
        corner_radius=5,
        cursor="hand2",
        command=confirm_coordinates,
    )
    btn_coords.grid(row=9, column=0)


def last() -> None:
    clear_window()

    label_title = ctk.CTkLabel(
        root,
        text="Pls Select ur language from the output of the AI (llm):",
        font=("Open Sans", 30, "bold"),
    )
    label_title.grid(row=0, column=0, padx=20, pady=(40, 10))

    language_selector = ctk.CTkComboBox(
        root,
        values=LANGUAGES,
        border_color="green",
        width=300,
        font=("Open Sans", 12),
        state="readonly",
    )
    language_selector.grid(row=1, column=0, pady=(0, 10))
    language_selector.set(LANGUAGES[0])

    feedback = ctk.CTkLabel(root, text="", text_color="white")
    feedback.grid(row=3, column=0, pady=(10, 0))

    def finish():
        clear_window()

        label_title = ctk.CTkLabel(root, text="Would you like to authorize a call to an api (library) to randomly display image backgrounds? (this exposes your IP address)?", font=("Open Sans", 30), justify="center", wraplength=900)
        label_title.grid(row=1, pady=(0, 15))

        label_info = ctk.CTkLabel(root, text="Lunar will download a free, royalty-free photo from [//]. This requires an internet connection, and //  will be able to see your IP address. You can change this anytime in Settings.", font=("Open Sans", 17), wraplength=700)
        label_info.grid(row=2)

        responses = ctk.CTkSwitch(root, text="Enable", onvalue="True", offvalue="False")
        responses.grid(row=3, pady=10)

        def save_choice_img():
            print("Oooh Shi")

            try:
                data = load_config()
                data["image-bg"] = responses.get()
                save_config(data)
                
                # Fonction pour attendre et lancer root.py en arrière-plan
                def bye():
                    time.sleep(5)  # Mets 20 si tu veux 20 secondes au lieu de 5
                    subprocess.Popen([sys.executable, "root.py"])
                    root.destroy()
                    print("Bye")

                
                threading.Thread(target=bye, daemon=True).start()

            except Exception as e:
                label_error = ctk.CTkLabel(root, text="Error: The data could not be saved properly.", font=("Open Sans", 19))
                label_error.grid(row=5)  # Corrigé à row=5 pour ne pas superposer avec le bouton

        btn_confirm = ctk.CTkButton(
            root,
            text="Confirm",
            fg_color=GREEN,
            text_color="white",
            corner_radius=5,
            cursor="hand2",
            command=save_choice_img,
            font=("Open Sans", 20),
            height=32
        )
        btn_confirm.grid(row=4, pady=12)



    def confirm_language() -> None:
        selected_language = language_selector.get()
        if selected_language not in LANGUAGES:
            feedback.configure(text="Error: Please select a language.", text_color="red")
            return


        data = load_config()
        data["language-content-llm"] = selected_language

        try:
            save_config(data)
        except OSError:
            feedback.configure(text="Error: Could not save your settings.", text_color="red")
            return

        btn_language.configure(state="disabled")
        feedback.configure(text="Please wait...", text_color="white")
        root.update()  

        try:
            run_computation()
        except Exception as e:
            feedback.configure(text=f"Error: {e}", text_color="red")
            btn_language.configure(state="normal")
            return

        try:
            data = load_config()
            data["did_setup"] = True
            save_config(data)
        except OSError:
            feedback.configure(text="Error: Could not save your settings.", text_color="red")
            btn_language.configure(state="normal")
            return

        feedback.configure(
            text="Thanks you! Welcome in Lunar...",
            text_color=GREEN,
        )
        
        finish()
        

    btn_language = ctk.CTkButton(
        root,
        text="Confirm",
        fg_color=GREEN,
        text_color="white",
        corner_radius=5,
        cursor="hand2",
        command=confirm_language,
    )
    btn_language.grid(row=2, column=0)



label_title = ctk.CTkLabel(
    root,
    text="Welcome in Lunar!",
    font=("Open Sans", 30, "bold"),
)
label_title.grid(row=1, pady=100)
label_info = ctk.CTkLabel(
    root,
    text="Your prayer times, always at hand. Lunar works privately and locally, with no account and no tracking.",
    font=("Open Sans", 14),
    cursor="hand2",
)
label_info.grid(row=4, pady=78)


btn_start = ctk.CTkButton(
    root,
    text="Start",
    fg_color=GREEN,
    text_color="white",
    corner_radius=5,
    cursor="hand2",
    command=method,
    font=("Open Sans", 20),
    height=32
)
btn_start.grid(row=3, column=0)




root.mainloop()