import json
from datetime import datetime, timedelta

import customtkinter as ctk
from utils import get_config_path

PRAYER_NAMES = {
    "fajr": "Fajr",
    "duhr": "Dhuhr",
    "asr": "Asr",
    "maghrib": "Maghrib",
    "icha": "Isha",
}

CARD_COLOR = "#333333"
ACCENT_COLOR = "#1F6AA5"
TIME_COLOR = "#2E8B57"
TIME_COLOR_NEXT = "#FFFFFF"

REFRESH_MS = 30_000


class Hometab:
    def __init__(self, parent_tab):
        self.frame = parent_tab
        self.config_data = self.load_config()

        self.cards = {}
        self.name_labels = {}
        self.time_labels = {}
        self.prayer_times = {}
        self._after_id = None

        self.build_ui()

        if self.prayer_times:
            self.update_highlight()
            self.frame.bind("<Destroy>", self._on_destroy)


    def build_ui(self):
        title = ctk.CTkLabel(
            self.frame,
            text="Prayer Times",
            font=("Open Sans", 22, "bold"),
        )
        title.pack(pady=(20, 10))

        prayers_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        prayers_frame.pack(pady=10, fill="x", padx=40)

        prayers = self.config_data.get("Prayer")
        if not prayers:
            error_label = ctk.CTkLabel(
                prayers_frame,
                text="No prayer schedule found in config.json. Check at APPDATA.",
            )
            error_label.pack(pady=10)
            return

        for key, display_name in PRAYER_NAMES.items():
            if key not in prayers:
                continue

            time_value = prayers[key]

            parsed = self.parse_time(time_value)
            if parsed is not None:
                self.prayer_times[key] = parsed

            card = ctk.CTkFrame(
                prayers_frame, corner_radius=8, fg_color=CARD_COLOR
            )
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
                text_color=TIME_COLOR,
            )
            time_label.pack(side="right", padx=20)

            self.cards[key] = card
            self.name_labels[key] = name_label
            self.time_labels[key] = time_label


    @staticmethod
    def parse_time(value):
        try:
            return datetime.strptime(str(value).strip(), "%H:%M").time()
        except ValueError:
            print(f"[Error...] Invalid prayer time: {value!r}")
            return None

    def get_next_prayer(self):
        now = datetime.now()

        ordered_keys = [k for k in PRAYER_NAMES if k in self.prayer_times]
        if not ordered_keys:
            return None, None

        for key in ordered_keys:
            dt = datetime.combine(now.date(), self.prayer_times[key])
            if dt > now:
                return key, dt

        first_key = ordered_keys[0]
        tomorrow = now.date() + timedelta(days=1)
        return first_key, datetime.combine(tomorrow, self.prayer_times[first_key])

    def update_highlight(self):
        next_key, _ = self.get_next_prayer()

        for key, card in self.cards.items():
            is_next = key == next_key
            card.configure(fg_color=ACCENT_COLOR if is_next else CARD_COLOR)
            self.time_labels[key].configure(
                text_color=TIME_COLOR_NEXT if is_next else TIME_COLOR
            )

        self._after_id = self.frame.after(REFRESH_MS, self.update_highlight)

    def _on_destroy(self, event):
        if event.widget is self.frame and self._after_id is not None:
            try:
                self.frame.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None


    def load_config(self):
        try:
            with get_config_path().open("r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            print(f"[Error...] Impossible to read config.json: {e}")
        return {}