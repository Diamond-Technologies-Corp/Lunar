import json
import customtkinter as ctk
from utils import get_config_path

BG_COLOR = "#2A05FA"
Dangerous = "#E62727"
TEXT_COLOR = "#FFFFFF"

class Settab:
    def __init__(self, parent_tab):
        self.frame = parent_tab
        
        self.widgets = {}
        self._after_id = None
        
        self.config_data = self.load_config()
        self.build_ui()

        self.frame.bind("<Destroy>", self._on_destroy)

    def load_config(self):
        try:
            with get_config_path().open("r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            print(f"[Error...] Impossible de lire config.json : {e}")
            return {}

    def build_ui(self):
        title = ctk.CTkLabel(
            self.frame,
            text="Settings",
            font=("Open Sans", 22, "bold"),
            text_color=TEXT_COLOR,
        )
        title.pack(pady=(20, 10))

        content_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        content_frame.pack(pady=10, fill="both", expand=True, padx=40)

        title_error = ctk.CTkLabel(self.frame, text="")
        
        action_button = ctk.CTkButton(
            content_frame,
            text="Reset all data",
            fg_color=Dangerous,
            command=self.reset,
            hover_color="#ED5959"
        )
        action_button.pack(pady=10)
        
        self.widgets["action_button"] = action_button

        about_us = ctk.CTkButton(
            self.frame,
            text="About Lunar..",
            fg_color=BG_COLOR,
            command=self.about
        )
        about_us.pack(pady=7)

        participate = ctk.CTkButton(
            self.frame,
            text="Participate to us survey? To improve Lunar.",
            fg_color="#09A43D",
            command=self.participate,
            hover_color="green"
        )
        participate.pack(pady=4)


    def participate(self):
        pop_up = ctk.CTkToplevel(self.frame)
        pop_up.geometry("800x500")
        pop_up.title("Want participate to our survey?")
        
        pop_up.grab_set() 

        label = ctk.CTkLabel(
            pop_up, 
            text="This can help us, to improve Lunar.", 
            font=("Open Sans", 18, "bold")
        )
        label.pack(pady=30)

        label_info = ctk.CTkLabel(
            pop_up,
            text="Check at https://docs.google.com/forms/d/e/1FAIpQLSdKr0zya93UPA40jWQsCu__6z1whD7xMMv-AzQoEP7wtODJ9Q/viewform.",
            font=("Open Sans", 18, "bold")
        )
        label_info.pack(pady=30)

        close_button = ctk.CTkButton(
            pop_up, 
            text="Close", 
            command=pop_up.destroy
        )
        close_button.pack(pady=10)

    def about(self):
        print("About us?")
        pop_up = ctk.CTkToplevel(self.frame)
        pop_up.geometry("300x200")
        pop_up.title("About Lunar")
        
        pop_up.grab_set() 

        label = ctk.CTkLabel(
            pop_up, 
            text="Lunar v1.5\nDeveloped by Diamond Technologies.", 
            font=("Open Sans", 16, "bold")
        )
        label.pack(pady=30)

        close_button = ctk.CTkButton(
            pop_up, 
            text="Close", 
            command=pop_up.destroy
        )
        close_button.pack(pady=10)

    def reset(self):
        print("We're going to reset all data.")
        try:
            config_path = get_config_path()
            
            with config_path.open("r", encoding="utf-8") as f:
                data = json.load(f)

            data["did_setup"] = False

            with config_path.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
                self.frame.winfo_toplevel().destroy()

                from main import main
                main()

                return True

        except Exception as e:
            print(f"[Error...] Reset failed: {e}")
            if "title_error" in self.widgets:
                self.widgets["title_error"].configure(text="An error occurred.")
            return False

    def start_loop(self):
        pass

    def _on_destroy(self, event):
        if event.widget is self.frame and self._after_id is not None:
            try:
                self.frame.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None