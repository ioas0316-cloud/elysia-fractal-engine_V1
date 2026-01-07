"""
Elysia Live Dashboard (실시간 대시보드)
=====================================

"상태를 보라. 파동을 느껴라."

실시간으로 엘리시아의 상태를 모니터링하는 웹 대시보드.

Features:
- GlobalHub 이벤트 스트림
- AutonomousOrchestrator 상태
- 학습 진행도
- 개념 밀도 시각화

Usage:
    python Core/Interface/live_dashboard.py
    → http://localhost:8080

[NEW 2025-12-15] LLM 독립 학습 시스템 모니터링
"""

import json
import logging
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger("LiveDashboard")


# Dashboard HTML template (embedded for simplicity)
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Elysia Live Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #e0e0e0;
            min-height: 100vh;
            padding: 20px;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 {
            font-size: 2.5em;
            background: linear-gradient(90deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .header p { color: #888; margin-top: 5px; }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }
        .card h2 {
            font-size: 1.2em;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .card h2 .icon { font-size: 1.5em; }
        
        .stat {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }
        .stat:last-child { border-bottom: none; }
        .stat .label { color: #888; }
        .stat .value { font-weight: bold; color: #48dbfb; }
        
        .phase {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
        }
        .phase.awakening { background: #ff6b6b; }
        .phase.learning { background: #48dbfb; }
        .phase.reflecting { background: #feca57; color: #333; }
        .phase.improving { background: #1dd1a1; }
        .phase.observing { background: #5f27cd; }
        .phase.dormant { background: #576574; }
        
        .event-log {
            max-height: 200px;
            overflow-y: auto;
            font-family: monospace;
            font-size: 0.85em;
            background: rgba(0, 0, 0, 0.3);
            padding: 10px;
            border-radius: 10px;
        }
        .event-log .event {
            padding: 5px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }
        .event-log .time { color: #888; }
        
        .refresh-btn {
            background: linear-gradient(90deg, #48dbfb, #1dd1a1);
            border: none;
            padding: 10px 25px;
            border-radius: 25px;
            color: #fff;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .refresh-btn:hover { transform: scale(1.05); }
        
        .status-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            display: inline-block;
            animation: pulse 2s infinite;
        }
        .status-dot.active { background: #1dd1a1; }
        .status-dot.inactive { background: #576574; animation: none; }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🌊 Elysia Live Dashboard</h1>
        <p>LLM 독립 자율 학습 시스템 모니터링</p>
    </div>
    
    <div class="grid">
        <!-- Autonomous Status -->
        <div class="card">
            <h2><span class="icon">🎼</span> Autonomous Orchestrator</h2>
            <div id="orchestrator-status">
                <div class="stat">
                    <span class="label">Phase</span>
                    <span class="value"><span id="phase" class="phase">loading...</span></span>
                </div>
                <div class="stat">
                    <span class="label">Cycles</span>
                    <span class="value" id="cycles">-</span>
                </div>
                <div class="stat">
                    <span class="label">Uptime</span>
                    <span class="value" id="uptime">-</span>
                </div>
                <div class="stat">
                    <span class="label">Running</span>
                    <span class="value">
                        <span id="running-dot" class="status-dot inactive"></span>
                    </span>
                </div>
            </div>
        </div>
        
        <!-- Learning Stats -->
        <div class="card">
            <h2><span class="icon">📚</span> Learning Progress</h2>
            <div class="stat">
                <span class="label">Concepts</span>
                <span class="value" id="concepts">-</span>
            </div>
            <div class="stat">
                <span class="label">Connections</span>
                <span class="value" id="connections">-</span>
            </div>
            <div class="stat">
                <span class="label">Wave Patterns</span>
                <span class="value" id="waves">-</span>
            </div>
            <div class="stat">
                <span class="label">Knowledge Gaps</span>
                <span class="value" id="gaps">-</span>
            </div>
        </div>
        
        <!-- GlobalHub Status -->
        <div class="card">
            <h2><span class="icon">🌐</span> GlobalHub (CNS)</h2>
            <div class="stat">
                <span class="label">Modules</span>
                <span class="value" id="modules">-</span>
            </div>
            <div class="stat">
                <span class="label">Events (1h)</span>
                <span class="value" id="events">-</span>
            </div>
            <div class="stat">
                <span class="label">Status</span>
                <span class="value">
                    <span id="hub-dot" class="status-dot active"></span> 온라인
                </span>
            </div>
        </div>
        
        <!-- Event Log -->
        <div class="card" style="grid-column: 1 / -1;">
            <h2><span class="icon">📜</span> Recent Events</h2>
            <div id="event-log" class="event-log">
                <div class="event"><span class="time">[Loading...]</span></div>
            </div>
        </div>
    </div>
    
    <div style="text-align: center; margin-top: 30px;">
        <button class="refresh-btn" onclick="fetchStatus()">🔄 Refresh</button>
    </div>
    
    <script>
        async function fetchStatus() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                
                // Update orchestrator
                const phase = document.getElementById('phase');
                phase.textContent = data.orchestrator.phase;
                phase.className = 'phase ' + data.orchestrator.phase;
                
                document.getElementById('cycles').textContent = data.orchestrator.cycles_completed;
                document.getElementById('uptime').textContent = 
                    Math.floor(data.orchestrator.uptime_seconds / 60) + ' min';
                
                const runningDot = document.getElementById('running-dot');
                runningDot.className = 'status-dot ' + (data.orchestrator.running ? 'active' : 'inactive');
                
                document.getElementById('gaps').textContent = data.orchestrator.knowledge_gaps;
                
                // Learning stats
                document.getElementById('concepts').textContent = data.learning.concepts || '0';
                document.getElementById('connections').textContent = data.learning.connections || '0';
                document.getElementById('waves').textContent = data.learning.waves || '0';
                
                // Hub stats
                document.getElementById('modules').textContent = data.hub.modules || '0';
                document.getElementById('events').textContent = data.hub.events || '0';
                
                // Event log
                const eventLog = document.getElementById('event-log');
                eventLog.innerHTML = data.events.map(e => 
                    `<div class="event"><span class="time">[${e.time}]</span> ${e.message}</div>`
                ).join('');
                
            } catch (err) {
                console.error('Failed to fetch status:', err);
            }
        }
        
        // Initial load
        fetchStatus();
        
        // Auto-refresh every 5 seconds
        setInterval(fetchStatus, 5000);
    </script>
</body>
</html>
"""


class DashboardState:
    """Singleton state for the dashboard."""
    
    def __init__(self):
        self.events = []
        self.learning_stats = {"concepts": 0, "connections": 0, "waves": 0}
        self.hub_stats = {"modules": 0, "events": 0}
        
    def add_event(self, message: str):
        """Add an event to the log."""
        timestamp = time.strftime("%H:%M:%S")
        self.events.insert(0, {"time": timestamp, "message": message})
        # Keep only last 50 events
        self.events = self.events[:50]

_dashboard_state = DashboardState()


def get_status() -> Dict[str, Any]:
    """Get current system status."""
    import sys
    sys.path.insert(0, r"c:\Elysia")
    
    # Orchestrator status
    orchestrator_status = {
        "phase": "dormant",
        "cycles_completed": 0,
        "uptime_seconds": 0,
        "running": False,
        "knowledge_gaps": 0
    }
    
    try:
        from Core.Evolution.Growth.Autonomy.autonomous_orchestrator import get_autonomous_orchestrator
        orchestrator = get_autonomous_orchestrator()
        orchestrator_status = orchestrator.get_status()
    except Exception as e:
        _dashboard_state.add_event(f"Orchestrator error: {e}")
    
    # Hub status
    hub_modules = 0
    try:
        from Core.Intelligence.Consciousness.Ether.global_hub import get_global_hub
        hub = get_global_hub()
        hub_modules = len(hub._modules) if hasattr(hub, '_modules') else 0
        _dashboard_state.hub_stats["modules"] = hub_modules
    except Exception:
        pass
    
    return {
        "orchestrator": orchestrator_status,
        "learning": _dashboard_state.learning_stats,
        "hub": _dashboard_state.hub_stats,
        "events": _dashboard_state.events[:20]
    }


class DashboardHandler(BaseHTTPRequestHandler):
    """HTTP handler for the dashboard."""
    
    def log_message(self, format, *args):
        """Suppress default logging."""
        pass
    
    def do_GET(self):
        if self.path == "/" or self.path == "/dashboard":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(DASHBOARD_HTML.encode('utf-8'))
            
        elif self.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            status = get_status()
            self.wfile.write(json.dumps(status).encode('utf-8'))
            
        else:
            self.send_response(404)
            self.end_headers()


def run_dashboard(port: int = 8080):
    """Run the live dashboard server."""
    server = HTTPServer(("", port), DashboardHandler)
    
    print("\n" + "=" * 60)
    print("🌊 ELYSIA LIVE DASHBOARD")
    print("=" * 60)
    print(f"\n🌐 Dashboard: http://localhost:{port}/")
    print("\nFeatures:")
    print("   • Autonomous Orchestrator status")
    print("   • Learning progress (LLM independent)")
    print("   • GlobalHub event stream")
    print("\nPress Ctrl+C to stop")
    print("=" * 60)
    
    _dashboard_state.add_event("Dashboard started")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped")
        server.server_close()


if __name__ == "__main__":
    import sys
    sys.path.insert(0, r"c:\Elysia")
    
    logging.basicConfig(level=logging.INFO)
    run_dashboard()
