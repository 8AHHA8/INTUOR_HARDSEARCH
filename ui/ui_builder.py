import tkinter as tk
import os
import string
import ctypes
from tkinter import filedialog
from ui.styles import BG_APP, BG_INPUT, TEXT_PRIMARY, TEXT_SECONDARY, ACCENT, FONT_TITLE, FONT_UI, FONT_ENTRY

def build_ui(app):
    lbl_title = tk.Label(app, text="//WYSZUKIWANIE", font=FONT_TITLE, bg=BG_APP, fg=TEXT_PRIMARY)
    lbl_title.pack(anchor="w", padx=40, pady=(30, 10))

    drive_frame = tk.Frame(app, bg=BG_APP)
    drive_frame.pack(fill="x", padx=40, pady=(0, 10))
    
    tk.Label(drive_frame, text="//WYBIERZ DYSK:", font=FONT_UI, bg=BG_APP, fg=TEXT_PRIMARY).pack(side="left", padx=(0, 10))

    DRIVE_REMOTE = 4
    available_drives = []
    for letter in string.ascii_uppercase[2:]:
        drive = f"{letter}:\\"
        if os.path.exists(drive):
            try:
                drive_type = ctypes.windll.kernel32.GetDriveTypeW(ctypes.c_wchar_p(drive))
                is_network = (drive_type == DRIVE_REMOTE)
                available_drives.append((drive, is_network))
            except:
                available_drives.append((drive, False))
    
    app.drive_btns = {}
    for drive, is_network in available_drives:
        btn_text = f"{drive} (Sieciowy)" if is_network else drive
        btn = tk.Button(drive_frame, text=btn_text, font=FONT_UI, bg=BG_INPUT, fg=TEXT_SECONDARY,
                        relief="flat", command=lambda d=drive: app._on_drive_clicked(d))
        btn.pack(side="left", padx=5)
        app.drive_btns[drive] = btn

    folder_frame = tk.Frame(app, bg=BG_APP)
    folder_frame.pack(fill="x", padx=40, pady=(5, 10))
    
    btn_folder = tk.Button(folder_frame, text="📁 WYBIERZ FOLDER", font=FONT_UI, bg=BG_INPUT, fg=TEXT_PRIMARY,
                           relief="flat", command=app._on_folder_clicked)
    btn_folder.pack(side="left")
    
    app.folder_label = tk.Label(folder_frame, text="Brak wybranego folderu", font=FONT_UI, bg=BG_APP, fg=TEXT_SECONDARY)
    app.folder_label.pack(side="left", padx=15)

    app.btn_clear_folder = tk.Button(folder_frame, text="✖ USUŃ FILTR FOLDERU", font=FONT_UI, bg=BG_INPUT, fg="#D32F2F",
                                      relief="flat", command=app._clear_folder_filter)
    app.btn_clear_folder.pack_forget()

    search_frame = tk.Frame(app, bg=BG_APP)
    search_frame.pack(fill="x", padx=40, pady=(10, 15))

    app.search_entry = tk.Entry(search_frame, font=FONT_ENTRY, bg=BG_INPUT, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, relief="flat")
    app.search_entry.pack(side="left", fill="x", expand=True, ipady=12, padx=(0, 15))
    app.search_entry.bind("<Return>", lambda e: app._perform_search())
    app.search_entry.bind("<KeyRelease>", app._on_search_key_release)

    btn_search = tk.Button(search_frame, text="SZUKAJ", font=FONT_UI, bg=BG_INPUT, fg=TEXT_PRIMARY,
                           relief="flat", command=app._perform_search, width=12)
    btn_search.pack(side="right", ipady=12)

    app.status_label = tk.Label(app, text="> SYSTEM GOTOWY.", font=("Consolas", 14), bg=BG_APP, fg=TEXT_PRIMARY)
    app.status_label.pack(anchor="w", padx=40, pady=5)

    app.results_container = tk.Frame(app, bg=BG_APP)
    app.results_container.pack(fill="both", expand=True, padx=40, pady=(10, 30))

    app.canvas = tk.Canvas(app.results_container, bg=BG_APP, highlightthickness=0)
    app.scrollbar = tk.Scrollbar(app.results_container, orient="vertical", command=app.canvas.yview)
    app.scrollable_frame = tk.Frame(app.canvas, bg=BG_APP)

    app.scrollable_frame.bind(
        "<Configure>",
        lambda e: app.canvas.configure(scrollregion=app.canvas.bbox("all"))
    )

    app.canvas.create_window((0, 0), window=app.scrollable_frame, anchor="nw")
    app.canvas.configure(yscrollcommand=app.scrollbar.set)

    app.canvas.pack(side="left", fill="both", expand=True)
    app.scrollbar.pack(side="right", fill="y")

    app.canvas.bind_all("<MouseWheel>", app._on_mousewheel)

    if "C:\\" in app.drive_btns:
        app._on_drive_clicked("C:\\")