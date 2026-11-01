import tkinter as tk
from core.db_connection import init_db
import ui.ui_builder as ui_builder
import ui.ui_handlers as ui_handlers

class IntuorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.conn = init_db()
        self.worker = None
        self.active_drive = None
        self.active_folder = None
        self.search_path_filter = None
        
        self.title("INTUOR_HARDSEARCH")
        self.geometry("1200x800")
        self.configure(bg="#050505")
        
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        ui_builder.build_ui(self)

    def _on_folder_clicked(self):
        ui_handlers.on_folder_clicked(self)

    def _clear_folder_filter(self):
        ui_handlers.clear_folder_filter(self)

    def _on_drive_clicked(self, drive):
        ui_handlers.on_drive_clicked(self, drive)

    def _on_mousewheel(self, event):
        ui_handlers.on_mousewheel(self, event)

    def _on_search_key_release(self, event):
        ui_handlers.on_search_key_release(self, event)

    def _perform_search(self):
        ui_handlers.perform_search(self)

    def _on_closing(self):
        ui_handlers.on_closing(self)

if __name__ == "__main__":
    app = IntuorApp()
    app.mainloop()