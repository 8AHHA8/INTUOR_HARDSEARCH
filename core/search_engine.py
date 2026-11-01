import os
import sqlite3
import re
import unicodedata

def strip_accents(text: str) -> str:
    text = unicodedata.normalize('NFKD', text)
    return ''.join(c for c in text if not unicodedata.combining(c))

def search(conn, query: str, limit: int = 50, raw: bool = False, extensions: set = None, path_filter: str = None):
    query_no_accents = strip_accents(query).strip()
    if not query_no_accents:
        return [] if raw else None

    words = re.findall(r'\w+', query_no_accents)
    if not words:
        return [] if raw else None

    fts_query = " AND ".join(f'"{w}"' for w in words)

    db_limit = limit * 100 if path_filter else limit * 10

    try:
        cursor = conn.execute(
            """
            SELECT file_path, content
            FROM docs_fts
            WHERE docs_fts MATCH ?
            ORDER BY rank
            LIMIT ?
            """,
            (fts_query, db_limit),
        )
        db_results = cursor.fetchall()
        conn.execute("PRAGMA shrink_memory;")
    except sqlite3.OperationalError:
        return []

    exact_results = []
    pattern_str = r'(?<!\w)' + re.escape(query_no_accents) + r'(?!\w)'
    regex = re.compile(pattern_str, re.IGNORECASE)

    normalized_filter = None
    if path_filter:
        normalized_filter = os.path.normpath(path_filter).lower()
        if not normalized_filter.endswith(os.sep):
            normalized_filter += os.sep

    for path, content in db_results:
        if normalized_filter:
            normalized_path = os.path.normpath(path).lower()
            if not normalized_path.startswith(normalized_filter):
                continue

        content_no_accents = strip_accents(content)
        match = regex.search(content_no_accents)
        
        if match:
            start = max(0, match.start() - 40)
            end = min(len(content), match.end() + 60)
            
            original_fragment = content[start:end].replace('\n', ' ').replace('\r', '')
            fragment_match = regex.search(strip_accents(original_fragment))
            
            if fragment_match:
                pre = original_fragment[:fragment_match.start()]
                hit = original_fragment[fragment_match.start():fragment_match.end()]
                post = original_fragment[fragment_match.end():]
                
                if start > 0: pre = "..." + pre
                if end < len(content): post = post + "..."
                
                final_fragment = f"{pre}>>>{hit}<<<{post}"
            else:
                final_fragment = "..." + original_fragment + "..."

            exact_results.append((path, final_fragment))

            if len(exact_results) >= limit:
                break

    return exact_results if raw else []