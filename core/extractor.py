from pathlib import Path

try:
    from pyxtxt import xtxt
except ImportError:
    xtxt = None

try:
    import pymupdf
except ImportError:
    try:
        import fitz as pymupdf
    except ImportError:
        pymupdf = None

def extract_text(file_path: Path) -> str:
    ext = file_path.suffix.lower()
    
    if ext == ".pdf" and pymupdf is not None:
        try:
            doc = pymupdf.open(str(file_path))
            text = "".join(page.get_text("text") + "\n" for page in doc)
            doc.close()
            if text.strip():
                return text
        except Exception:
            pass

    if xtxt is not None and ext != ".pdf":
        try:
            content = xtxt(str(file_path))
            if content:
                return content
        except Exception:
            pass
            
    if ext == ".txt":
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read(100000)
                if text.strip():
                    return text
        except Exception:
            pass
            
        try:
            with open(file_path, 'r', encoding='cp1250', errors='ignore') as f:
                text = f.read(100000)
                if text.strip():
                    return text
        except Exception:
            pass
            
    return ""