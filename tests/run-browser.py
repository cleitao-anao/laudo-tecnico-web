"""Run after the C# suite. Uses installed Chrome/Edge and Python standard library."""
import functools
import http.server
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import threading

root = Path(__file__).resolve().parents[2]

# O laudo em arquivo único precisa acompanhar o site (index.html + style.css + script.js)
check = subprocess.run([sys.executable, str(root / 'laudo-tecnico-web' / 'gerar-arquivo-unico.py'), '--check'])
if check.returncode != 0:
    raise SystemExit(1)
candidates = [Path(os.environ.get('PROGRAMFILES', 'C:/Program Files')) / 'Google/Chrome/Application/chrome.exe',
              Path(os.environ.get('PROGRAMFILES(X86)', 'C:/Program Files (x86)')) / 'Microsoft/Edge/Application/msedge.exe']
browser = next((p for p in candidates if p.exists()), None)
if not browser:
    raise SystemExit('Chrome ou Edge não encontrado.')

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(root)))
threading.Thread(target=server.serve_forever, daemon=True).start()
try:
    with tempfile.TemporaryDirectory(prefix='laudo-browser-') as profile:
        url = f'http://127.0.0.1:{server.server_port}/laudo-tecnico-web/tests/integration.html'
        result = subprocess.run([str(browser), '--headless=new', '--disable-gpu', '--no-first-run',
            '--disable-background-networking', '--disable-component-update', '--no-proxy-server',
            '--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE 127.0.0.1',
            '--user-data-dir=' + profile, '--dump-dom', '--virtual-time-budget=15000', url],
            capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=50,
            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        match = re.search(r'<pre id="result">(.*?)</pre>', result.stdout, re.S)
        message = match.group(1) if match else result.stderr[-2000:]
        print(message)
        if not message.startswith('PASS:'):
            raise SystemExit(1)
finally:
    server.shutdown()
