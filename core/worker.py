import threading
from core.indexer import index_folder_parallel

class IndexWorker(threading.Thread):
    def __init__(self, conn, paths, on_progress=None, on_done=None):
        super().__init__()
        self.conn = conn
        self.paths = paths
        self._is_running = True
        self.on_progress = on_progress
        self.on_done = on_done

    def stop(self):
        self._is_running = False

    def run(self):
        total_indexed = 0
        total_errors = 0
        total_time = 0.0
        
        for p in self.paths:
            if not self._is_running:
                break
                
            if self.on_progress:
                self.on_progress(f"Scanning: {p}...")
            
            def done_cb(i, e, t):
                nonlocal total_indexed, total_errors, total_time
                total_indexed += i
                total_errors += e
                total_time += t

            index_folder_parallel(
                self.conn, p,
                on_progress=lambda m: self.on_progress(m) if self.on_progress else None,
                on_done=done_cb
            )
            
        if self._is_running and self.on_done:
            self.on_done(total_indexed, total_errors, total_time)