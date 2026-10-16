"""Lokalni pregled: python -X utf8 scripts/dev.py. Ctrl+C za prekid."""
import http.server
import os
from pathlib import Path
import subprocess
import sys
import threading
import time
import webbrowser
ROOT = Path(__file__).resolve().parent.parent

def build():
    return subprocess.run([sys.executable, '-X', 'utf8', str(ROOT/'scripts/build.py')], cwd=ROOT).returncode == 0

def snapshot():
    return {str(p): p.stat().st_mtime_ns for folder in ('content','public','scripts') for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in str(p)}

def watch():
    previous=snapshot()
    while True:
        time.sleep(1)
        current=snapshot()
        if current != previous:
            previous=current
            if build(): print('Izmene su spremne. Osvežite stranicu u pregledaču.', flush=True)

if build():
    os.chdir(ROOT/'dist')
    server=http.server.ThreadingHTTPServer(('127.0.0.1', 8000), http.server.SimpleHTTPRequestHandler)
    threading.Thread(target=watch,daemon=True).start()
    print('Lokalni pregled: http://localhost:8000 — Ctrl+C za prekid',flush=True)
    webbrowser.open('http://localhost:8000')
    try: server.serve_forever()
    except KeyboardInterrupt: server.server_close()
