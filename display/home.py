import json
from pathlib import Path

import customtkinter as ctk
from utils import resource_path


class Hometab:
    def __init__(self, parent_tab):
        self.frame = parent_tab
        self.config_data = self.load_config()

        title = ctk.CTkLabel(
            self.frame,
            text="Horaires des Prières",
            font=("Open Sans", 22, "bold"),
        )
        title.pack(pady=(20, 10))

        prayers_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        prayers_frame.pack(pady=10, fill="x", padx=40)

        if "Prayer" in self.config_data:
            prayers = self.config_data["Prayer"]

            prayer_names = {
                "fajr": "Fajr",
                "duhr": "Dhuhr",
                "asr": "Asr",
                "maghrib": "Maghrib",
                "icha": "Isha",
            }

            for key, display_name in prayer_names.items():
                if key in prayers:
                    time_value = prayers[key]

                    card = ctk.CTkFrame(prayers_frame, corner_radius=8)
                    card.pack(pady=5, fill="x", ipady=5)

                    name_label = ctk.CTkLabel(
                        card,
                        text=display_name,
                        font=("Open Sans", 16, "bold"),
                    )
                    name_label.pack(side="left", padx=20)

                    time_label = ctk.CTkLabel(
                        card,
                        text=f"{time_value}h",
                        font=("Open Sans", 16),
                        text_color="#2E8B57",
                    )
                    time_label.pack(side="right", padx=20)
        else:
            error_label = ctk.CTkLabel(
                prayers_frame,
                text="⚠️ Aucun horaire de prière trouvé dans config.json",
            )
            error_label.pack(pady=10)

    def load_config(self):
        try:
            config_path = Path(__file__).resolve().parent.parent / "config.json"
            with config_path.open("r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            print(f"[Erreur] Impossible de lire config.json : {e}")
        return {}