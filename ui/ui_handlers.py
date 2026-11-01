import os
import gc
from tkinter import messagebox, filedialog
from core.db_connection import get_setting, set_setting
from core.search_engine import search
from core.worker import IndexWorker
from ui.ui_results import create_result_card
from ui.styles import BG_INPUT, TEXT_SECONDARY, ACCENT

def on_folder_clicked(app):
    folder = filedialog.askdirectory(title="Wybierz folder do przeszukania")
    if folder:
        folder = os.path.normpath(folder)
        app.active_folder = folder
        app.search_path_filter = folder
        app.folder_label.config(text=folder, fg=ACCENT)
        app.btn_clear_folder.pack(side="left", padx=5)
        
        for d, btn in app.drive_btns.items():
            btn.config(bg=BG_INPUT, fg=TEXT_SECONDARY)
        app.active_drive = None
        
        start_background_indexing(app, [folder])

def clear_folder_filter(app):
    app.active_folder = None
    app.search_path_filter = None
    app.folder_label.config(text="Brak wybranego folderu", fg=TEXT_SECONDARY)
    app.btn_clear_folder.pack_forget()
    
    if not app.active_drive:
        if "C:\\" in app.drive_btns:
            on_drive_clicked(app, "C:\\")
    set_status(app, "USUNIĘTO FILTR FOLDERU. WYSZUKIWANIE GLOBALNE.")

def on_drive_clicked(app, drive):
    app.active_folder = None
    app.search_path_filter = None
    app.folder_label.config(text="Brak wybranego folderu", fg=TEXT_SECONDARY)
    app.btn_clear_folder.pack_forget()

    for d, btn in app.drive_btns.items():
        btn.config(bg=BG_INPUT, fg=TEXT_SECONDARY)
    
    app.drive_btns[drive].config(bg=ACCENT, fg="#050505")
    app.active_drive = drive
    
    scanned_key = f"scanned_{drive.replace(':', '')}"
    is_scanned = get_setting(app.conn, scanned_key)
    
    if is_scanned:
        set_status(app, f"DYSK {drive} ZOSTAŁ JUŻ ZESKANOWANY. POMIJAM SKANOWANIE.")
        return
        
    start_background_indexing(app, [drive])

def on_mousewheel(app, event):
    app.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

def set_status(app, text):
    app.status_label.config(text=f"> {text}")

def on_search_key_release(app, event):
    if not app.search_entry.get().strip():
        if app.scrollable_frame.winfo_children():
            for widget in app.scrollable_frame.winfo_children():
                widget.destroy()
            gc.collect()
            set_status(app, "WPROWADŹ NOWE ZAPYTANIE.")

def perform_search(app):
    query = app.search_entry.get().strip()
    if not query:
        return
    
    for widget in app.scrollable_frame.winfo_children():
        widget.destroy()
    gc.collect()
    set_status(app, "SZUKANIE...")

    try:
        results = search(app.conn, query, limit=30, raw=True, extensions=None, path_filter=app.search_path_filter)
    except Exception as e:
        messagebox.showerror("Błąd", str(e))
        return

    if not results:
        if app.search_path_filter:
            global_results = search(app.conn, query, limit=1, raw=True, extensions=None, path_filter=None)
            if global_results:
                set_status(app, f"BRAK W TYM FOLDERZE. ZNALEZIONO W INNYCH LOKALIZACJACH.")
                return
        
        set_status(app, "BRAK WYNIKÓW.")
        return

    for path, fragment in results:
        if fragment:
            clean_fragment = fragment.replace('\n', ' ').replace('\r', '')
        else:
            clean_fragment = ""

        create_result_card(app, os.path.dirname(path), os.path.basename(path), clean_fragment)
        
    set_status(app, f"ZNALEZIONO {len(results)} PLIKÓW.")
    gc.collect()

def start_background_indexing(app, paths):
    if app.worker and app.worker.is_alive():
        app.worker.stop()
        
    set_status(app, f"SKANOWANIE: {paths[0]} W TLE...")
    app.worker = IndexWorker(
        app.conn, 
        paths, 
        on_progress=lambda m: app.after(0, lambda: set_status(app, m)), 
        on_done=lambda i, e, t: app.after(0, lambda: on_index_done(app, i, e, t, paths[0]))
    )
    app.worker.start()

def on_index_done(app, indexed, errors, elapsed, scanned_path):
    if scanned_path.endswith(":\\"):
        scanned_key = f"scanned_{scanned_path.replace(':', '')}"
        set_setting(app.conn, scanned_key, "1")
        
    if indexed == 0:
         set_status(app, "ZAKTUALNIONO. PLIKI BYŁY JUŻ W BAZIE. GOTOWY.")
    else:
         set_status(app, f"DODANO: {indexed} NOWYCH PLIKÓW. GOTOWY.")
    gc.collect()

def on_closing(app):
    try:
        if app.worker and app.worker.is_alive():
            app.worker.stop()
        app.conn.close()
    except:
        pass
    finally:
        os._exit(0)