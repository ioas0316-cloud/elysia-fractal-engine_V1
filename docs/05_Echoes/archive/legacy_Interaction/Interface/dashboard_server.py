"""
엘리시아 대시보드 서버
Elysia Dashboard Server

Simple web server to display the dashboard.
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
from pathlib import Path


class DashboardHandler(SimpleHTTPRequestHandler):
    """Custom handler for dashboard"""
    
    def __init__(self, *args, **kwargs):
        # Set the directory to serve files from
        super().__init__(*args, directory=str(Path(__file__).parent.parent), **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/' or self.path == '/dashboard':
            self.path = '/static/templates/dashboard.html'
        return super().do_GET()
    
    def end_headers(self):
        """Add CORS headers"""
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()


def run_dashboard(port=8080):
    """Run the dashboard server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, DashboardHandler)
    
    print("=" * 60)
    print("🎨 Elysia Dashboard Server")
    print("=" * 60)
    print(f"🌐 Dashboard: http://localhost:{port}/dashboard")
    print(f"📖 Direct: http://localhost:{port}/static/templates/dashboard.html")
    print()
    print("⚠️  Make sure the API server is running on port 8000!")
    print("   Start API: python Core/Interface/api_server.py")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Dashboard server stopped")
        httpd.server_close()


if __name__ == "__main__":
    run_dashboard()
