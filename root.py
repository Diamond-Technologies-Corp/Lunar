import customtkinter as ctk
from update import apply_update, check_for_updates, launch
from PIL import Image
from display.home import Hometab
from display.settings import Settab
from utils import resource_path


def build():

    ctk.set_appearance_mode("dark")

    root = ctk.CTk()
    root.title("Lunar")
    root.geometry("1000x580")
    root.minsize(800, 500)
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.iconbitmap(resource_path("assets/img/Lunar-icon.ico"))

    raw_image = Image.open(resource_path("assets/img/root-blur.jpg"))
    bg_image = ctk.CTkImage(light_image=raw_image, dark_image=raw_image, size=(1000, 580))
    bg_label = ctk.CTkLabel(root, image=bg_image, text="")
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def on_resize(event):
        
        if event.widget == root:
            bg_image.configure(size=(event.width, event.height))

    root.bind("<Configure>", on_resize)

    header_frame = ctk.CTkFrame(root, fg_color="transparent")
    header_frame.grid(row=0, column=0, pady=(20, 5))

    label_title = ctk.CTkLabel(
        header_frame, 
        text="Lunar", 
        font=("Montserrat", 26, "bold"), 
        text_color="#FFFFFF"
    )
    label_title.pack(side="left", padx=5)

    badge_version = ctk.CTkLabel(
        header_frame,
        text="v1.4",
        font=("Open Sans", 11, "bold"),
        fg_color="#00C4EE",
        text_color="#121212",
        corner_radius=10,
        width=45,
        height=20
    )
    badge_version.pack(side="left", padx=5)


    main_card = ctk.CTkFrame(
        root,
        corner_radius=20,
        fg_color="#181A1D",
        border_width=1,
        border_color="#2A2E33"
    )
    main_card.grid(row=2, column=0, padx=30, pady=(5, 20), sticky="nsew")
    main_card.grid_rowconfigure(1, weight=1)
    main_card.grid_columnconfigure(0, weight=1)


    def select_tab(value):
        if value == "Home":
            frame_settings.pack_forget()
            frame_home.pack(fill="both", expand=True, padx=20, pady=15)
        elif value == "Settings":
            frame_home.pack_forget()
            frame_settings.pack(fill="both", expand=True, padx=20, pady=15)

    nav_switcher = ctk.CTkSegmentedButton(
        main_card,
        values=["Home", "Settings"],
        command=select_tab,
        selected_color="#00C4EE",
        selected_hover_color="#00A3C7",
        unselected_color="#23262A",
        unselected_hover_color="#2E3238",
        text_color="#FFFFFF",
        font=("Open Sans", 13, "bold"),
        corner_radius=12,
        height=36,
        width=260
    )
    nav_switcher.grid(row=0, column=0, pady=(15, 5))

    # ZONE DE CONTENU DYNAMIQUE
    content_area = ctk.CTkFrame(main_card, fg_color="transparent")
    content_area.grid(row=1, column=0, sticky="nsew")

    frame_home = ctk.CTkFrame(content_area, fg_color="transparent")
    frame_settings = ctk.CTkFrame(content_area, fg_color="transparent")

    # Chargement des onglets
    Hometab(frame_home)
    Settab(frame_settings)

    # Onglet par défaut
    nav_switcher.set("Home")
    select_tab("Home")

    # --- SYSTÈME DE MISE À JOUR ---
    def updating():
        print("Starting Verification...")
        result = check_for_updates()

        if result and result.get("update_available"):
            banner = ctk.CTkFrame(root, fg_color="#1E232A", corner_radius=12, border_width=1, border_color="#00C4EE")
            banner.grid(row=3, column=0, padx=40, pady=(0, 15), sticky="ew")
            banner.grid_columnconfigure(0, weight=1)

            msg = ctk.CTkLabel(
                banner,
                text=f"🚀 A new update (v{result['latest_version']}) is available!",
                font=("Open Sans", 13, "bold"),
                text_color="#FFFFFF"
            )
            msg.grid(row=0, column=0, padx=15, pady=10, sticky="w")

            btn_box = ctk.CTkFrame(banner, fg_color="transparent")
            btn_box.grid(row=0, column=1, padx=10, pady=5)

            def Yes():
                zip_path = launch()
                if zip_path:
                    apply_update(zip_path)

            def No():
                banner.destroy()

            install_btn = ctk.CTkButton(
                btn_box,
                text="Update now",
                fg_color="#00C4EE",
                hover_color="#00A3C7",
                text_color="#121212",
                font=("Open Sans", 12, "bold"),
                corner_radius=8,
                width=110,
                command=Yes
            )
            install_btn.pack(side="left", padx=5)

            no_btn = ctk.CTkButton(
                btn_box,
                text="Later",
                fg_color="#2E3238",
                hover_color="#3A3E45",
                text_color="#AAAAAA",
                font=("Open Sans", 12),
                corner_radius=8,
                width=70,
                command=No
            )
            no_btn.pack(side="left", padx=5)

    root.after(500, updating)
    root.mainloop()