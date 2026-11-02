import tkinter as tk
import os
from ui.styles import BG_INPUT, TEXT_PRIMARY, ACCENT, FONT_HEADER, FONT_CARD, FONT_CARD_BOLD
from tkinter import messagebox

def create_result_card(app, path, name, fragment):
    full_path = os.path.join(path, name)

    card = tk.Frame(app.scrollable_frame, bg=BG_INPUT, padx=25, pady=20)
    card.pack(fill="x", pady=8)
    
    lbl_path_head = tk.Label(card, text="//PATH:", font=FONT_HEADER, bg=BG_INPUT, fg=TEXT_PRIMARY, anchor="w")
    lbl_path_head.pack(fill="x")
    lbl_path = tk.Label(card, text=path, font=FONT_CARD, bg=BG_INPUT, fg=TEXT_PRIMARY, anchor="w")
    lbl_path.pack(fill="x", pady=(10, 15)) 
    
    lbl_name_head = tk.Label(card, text="//NAME:", font=FONT_HEADER, bg=BG_INPUT, fg=TEXT_PRIMARY, anchor="w")
    lbl_name_head.pack(fill="x")
    lbl_name = tk.Label(card, text=name, font=FONT_CARD, bg=BG_INPUT, fg=TEXT_PRIMARY, anchor="w")
    lbl_name.pack(fill="x", pady=(10, 15))

    lbl_snippet_head = None
    text_widget = None
    
    if fragment:
        lbl_snippet_head = tk.Label(card, text="//LOCATION:", font=FONT_HEADER, bg=BG_INPUT, fg=TEXT_PRIMARY, anchor="w")
        lbl_snippet_head.pack(fill="x")
        
        text_widget = tk.Text(card, font=FONT_CARD, bg=BG_INPUT, fg=TEXT_PRIMARY, 
                              wrap="word", height=1, relief="flat", highlightthickness=0)
        text_widget.pack(fill="x", pady=(10, 0))
        
        parts = fragment.split('>>>')
        for i, part in enumerate(parts):
            if i == 0:
                text_widget.insert(tk.END, part)
            else:
                if '<<<' in part:
                    highlight, rest = part.split('<<<', 1)
                    text_widget.insert(tk.END, highlight, "highlight")
                    text_widget.insert(tk.END, rest)
                else:
                    text_widget.insert(tk.END, part)
        
        text_widget.tag_configure("highlight", foreground=ACCENT, font=FONT_CARD_BOLD)
        
        text_widget.update_idletasks()
        lines = int(text_widget.index('end-1c').split('.')[0])
        text_widget.config(height=lines)
        
        text_widget.config(state="disabled")

    def open_item(event):
        try:
            import subprocess
            subprocess.run(["explorer", "/select,", full_path])
            os.startfile(full_path)
        except Exception as e:
            messagebox.showerror("Open Error", f"Cannot open file:\n{e}")

    card.bind("<Double-1>", open_item)
    lbl_path_head.bind("<Double-1>", open_item)
    lbl_path.bind("<Double-1>", open_item)
    lbl_name_head.bind("<Double-1>", open_item)
    lbl_name.bind("<Double-1>", open_item)
    
    if lbl_snippet_head:
        lbl_snippet_head.bind("<Double-1>", open_item)
    if text_widget:
        text_widget.bind("<Double-1>", open_item)