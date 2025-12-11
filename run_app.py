"""Simple HTTP server to run the HTML app."""
import http.server
import socketserver
import webbrowser
from pathlib import Path

PORT = 3000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='public', **kwargs)

print(f"🚀 Starting server at http://localhost:{PORT}")
print(f"📂 Serving files from: {Path('public').absolute()}")
print("\n✨ Opening browser...")

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    webbrowser.open(f'http://localhost:{PORT}')
    print(f"\n✅ Server running! Press Ctrl+C to stop.\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped.")
