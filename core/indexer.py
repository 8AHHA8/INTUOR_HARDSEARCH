import os
import sqlite3
import time
import concurrent.futures
from pathlib import Path
from core.extractor import extract_text

ALLOWED_EXT = {".pdf", ".docx", ".doc", ".xlsx", ".xls", ".pptx", ".ppt", ".odt", ".txt"}

def process_single_file(args):
    conn, path_str, mtime = args
    path = Path(path_str)
    try:
        cursor = conn.execute("SELECT mtime FROM file_state WHERE file_path = ?", (path_str,))
        row = cursor.fetchone()
        if row and abs(row[0] - mtime) < 1.0:
            return None

        content = extract_text(path)
        if content and content.strip():
            return (path_str, content, mtime)
        else:
            return (path_str, None, mtime)
    except Exception:
        return None

def index_folder_parallel(conn, root_path: str, on_progress=None, on_done=None):
    root = Path(root_path)
    if not root.exists():
        if on_done:
            on_done(0, 1, 0.0)
        return

    indexed = errors = 0
    start = time.time()
    
    files_to_process = []
    stack = [root]
    while stack:
        current_dir = stack.pop()
        try:
            with os.scandir(current_dir) as it:
                for entry in it:
                    try:
                        if entry.is_dir(follow_symlinks=False):
                            stack.append(Path(entry.path))
                        elif entry.is_file(follow_symlinks=False):
                            path = Path(entry.path)
                            if path.suffix.lower() in ALLOWED_EXT:
                                try:
                                    mtime = entry.stat().st_mtime
                                    files_to_process.append((conn, str(path), mtime))
                                except OSError:
                                    pass
                    except (PermissionError, OSError):
                        continue
        except (PermissionError, OSError):
            continue

    total_files = len(files_to_process)
    if on_progress:
        on_progress(f"Znaleziono {total_files} plików. Rozpoczynam analizę...")

    batch = []
    last_update_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(process_single_file, f): f for f in files_to_process}
        
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            try:
                result = future.result()
                if result:
                    path_str, content, mtime = result
                    if content:
                        batch.append((path_str, content))
                        indexed += 1
                    
                    conn.execute(
                        "INSERT OR REPLACE INTO file_state (file_path, mtime) VALUES (?, ?)",
                        (path_str, mtime)
                    )
                    
                    if len(batch) >= 50:
                        conn.executemany(
                            "INSERT INTO docs_fts(file_path, content) VALUES (?, ?)",
                            batch
                        )
                        batch.clear()
                
                current_time = time.time()
                if on_progress and (current_time - last_update_time > 0.25):
                    on_progress(f"[Analiza] Przetworzono {i+1}/{total_files}...")
                    last_update_time = current_time

            except sqlite3.ProgrammingError:
                break
            except Exception:
                pass

    try:
        if batch:
            conn.executemany("INSERT INTO docs_fts(file_path, content) VALUES (?, ?)", batch)
        conn.commit()
        conn.execute("PRAGMA shrink_memory;")
    except Exception:
        pass

    elapsed = time.time() - start
    if on_done:
        on_done(indexed, errors, elapsed)