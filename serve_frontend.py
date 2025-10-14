import http.server
import socketserver
import webbrowser
import os

# Get the current directory and frontend path
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(current_dir, 'frontend')

print(f"Current directory: {current_dir}")
print(f"Frontend directory: {frontend_dir}")

# Check if frontend directory exists
if not os.path.exists(frontend_dir):
    print(f"ERROR: Frontend directory not found at: {frontend_dir}")
    print("Please make sure you have a 'frontend' folder with index.html")
    exit(1)

# Change to the frontend directory
os.chdir(frontend_dir)

PORT = 3000  # CHANGED TO 3000

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

print(f"🌐 Frontend server running at: http://localhost:{PORT}")
print("📁 Serving files from:", os.getcwd())
print("Opening browser automatically...")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    webbrowser.open(f'http://localhost:{PORT}')
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
