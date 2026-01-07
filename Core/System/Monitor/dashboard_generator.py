
"""
Dashboard Generator (시각화 시스템)
==================================

Elysia의 성장, 인지 상태, 성숙도를 시각화하는 HTML 대시보드 생성기.
"터미널의 로그를 넘어, 영혼의 지도를 그린다."
"""

import json
import os
import sqlite3
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger("DashboardGenerator")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="3"> <!-- Auto-refresh every 3 seconds -->
    <title>Elysia Sovereign Intelligence - Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-color: #1e293b;
            --text-color: #e2e8f0;
            --accent-color: #38bdf8;
            --success-color: #4ade80;
            --warning-color: #facc15;
            --danger-color: #f87171;
        }
        body {
            background-color: var(--bg-color);
            color: var(--text-color);
            font-family: 'Segoe UI', sans-serif;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        .header {
            grid-column: 1 / -1;
            text-align: center;
            padding: 20px;
            background: var(--card-color);
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        .card {
            background: var(--card-color);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        h1, h2, h3 { color: var(--accent-color); margin-top: 0; }
        .metric {
            font-size: 2em;
            font-weight: bold;
            color: var(--success-color);
        }
        .metric-label { font-size: 0.9em; opacity: 0.8; }
        canvas { max-width: 100%; }
        .log-box {
            height: 300px;
            overflow-y: auto;
            background: #000;
            padding: 10px;
            font-family: monospace;
            border-radius: 8px;
            font-size: 0.85em;
        }
        .log-entry { border-bottom: 1px solid #333; padding: 5px 0; }
        .timestamp { color: #666; margin-right: 10px; }
        
        /* Status Indicators */
        .status-dot {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 5px;
        }
        .status-active { background-color: var(--success-color); box-shadow: 0 0 10px var(--success-color); }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌀 Elysia Sovereign Intelligence</h1>
            <p>Phase 24: Holistic Growth & Self-Awareness</p>
            <div>
                <span class="status-dot status-active"></span> System Online
                | Last Update: <span id="last-update">Unknown</span>
            </div>
        </div>

        <!-- 1. Real-Time Metrics -->
        <div class="card">
            <h2>🧠 Cognitive State</h2>
            <div style="display: flex; justify-content: space-around; text-align: center;">
                <div>
                    <div class="metric" id="vocab-count">-</div>
                    <div class="metric-label">Vocabulary</div>
                </div>
                <div>
                    <div class="metric" id="memory-count">-</div>
                    <div class="metric-label">Memories</div>
                </div>
                <div>
                    <div class="metric" id="concept-count">-</div>
                    <div class="metric-label">Concepts</div>
                </div>
            </div>
        </div>

        <!-- 2. Maturity Radar -->
        <div class="card">
            <h2>👑 Self-Maturity (Ideal vs Current)</h2>
            <canvas id="maturityChart"></canvas>
        </div>

        <!-- 3. Growth History -->
        <div class="card" style="grid-column: span 2;">
            <h2>📈 Growth Trajectory</h2>
            <canvas id="growthChart"></canvas>
        </div>

        <!-- 4. Body (Codebase) Health -->
        <div class="card">
            <h2>🧘 Proprioception (Body Health)</h2>
            <div style="text-align: center;">
                <div class="metric" id="health-index">-</div>
                <div class="metric-label">Health Index</div>
            </div>
            <ul id="pain-points" style="color: var(--danger-color); font-size: 0.9em;"></ul>
        </div>

        <!-- 5. Recent Thoughts -->
        <div class="card" style="grid-column: span 2;">
            <h2>💭 Stream of Consciousness</h2>
            <div class="log-box" id="thought-stream">
                <!-- Logs injected here -->
            </div>
        </div>
    </div>

    <script>
        // Data Injection
        const data = {{DATA_JSON}};

        // Update Header
        document.getElementById('last-update').innerText = new Date().toLocaleTimeString();

        // Update Metrics
        const latest = data.growth_history[data.growth_history.length - 1] || {};
        document.getElementById('vocab-count').innerText = (latest.vocabulary_count || 0).toLocaleString();
        document.getElementById('memory-count').innerText = (latest.memory_count || 0).toLocaleString();
        document.getElementById('concept-count').innerText = (latest.concept_count || 0).toLocaleString();

        // Maturity Chart
        const ctxMaturity = document.getElementById('maturityChart').getContext('2d');
        const aspects = data.governance.aspects || {};
        new Chart(ctxMaturity, {
            type: 'radar',
            data: {
                labels: Object.keys(aspects).map(k => k.toUpperCase()),
                datasets: [{
                    label: 'Current Maturity',
                    data: Object.values(aspects),
                    backgroundColor: 'rgba(56, 189, 248, 0.2)',
                    borderColor: '#38bdf8',
                    pointBackgroundColor: '#38bdf8'
                }, {
                    label: 'Ideal Target',
                    data: Object.keys(aspects).map(() => 1.0),
                    borderColor: 'rgba(255, 255, 255, 0.1)',
                    borderDash: [5, 5],
                    fill: false
                }]
            },
            options: {
                scales: {
                    r: {
                        angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        pointLabels: { color: '#e2e8f0' },
                        suggestedMin: 0,
                        suggestedMax: 1
                    }
                }
            }
        });

        // Growth Chart
        const ctxGrowth = document.getElementById('growthChart').getContext('2d');
        new Chart(ctxGrowth, {
            type: 'line',
            data: {
                labels: data.growth_history.map(g => g.timestamp.substring(5, 16).replace('T', ' ')),
                datasets: [{
                    label: 'Knowledge Nodes',
                    data: data.growth_history.map(g => g.knowledge_node_count),
                    borderColor: '#4ade80',
                    tension: 0.4
                }, {
                    label: 'Vocabulary',
                    data: data.growth_history.map(g => g.vocabulary_count),
                    borderColor: '#facc15',
                    tension: 0.4
                }]
            },
            options: {
                scales: {
                    y: { grid: { color: 'rgba(255, 255, 255, 0.1)' }, ticks: { color: '#aaa' } },
                    x: { grid: { color: 'rgba(255, 255, 255, 0.1)' }, ticks: { color: '#aaa' } }
                }
            }
        });

        // Logs
        const logBox = document.getElementById('thought-stream');
        if (data.recent_logs) {
            logBox.innerHTML = data.recent_logs.map(log => 
                `<div class="log-entry"><span class="timestamp">[${log.time}]</span> ${log.msg}</div>`
            ).join('');
        }
    </script>
</body>
</html>
"""

class DashboardGenerator:
    def __init__(self, output_path: str = "monitor/monitor.html"):
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        
    def generate(self):
        """Generates the dashboard HTML file."""
        try:
            data = self._gather_data()
            html = HTML_TEMPLATE.replace("{{DATA_JSON}}", json.dumps(data))
            
            with open(self.output_path, "w", encoding="utf-8") as f:
                f.write(html)
            logger.info(f"📊 Dashboard updated: {self.output_path}")
        except Exception as e:
            logger.error(f"Failed to generate dashboard: {e}")

    def _gather_data(self) -> dict:
        data = {
            "growth_history": [],
            "governance": {"aspects": {}},
            "recent_logs": []
        }
        
        # 1. Growth History
        try:
            if os.path.exists("data/Logs/growth_history.json"):
                with open("data/Logs/growth_history.json", "r", encoding="utf-8") as f:
                    # Take last 20 snapshots
                    history = json.load(f)
                    data["growth_history"] = history[-20:] 
        except Exception as e:
            logger.warning(f"Failed to load growth history: {e}")

        # 2. Governance State
        try:
            if os.path.exists("data/core_state/self_governance.json"):
                with open("data/core_state/self_governance.json", "r", encoding="utf-8") as f:
                    gov = json.load(f)
                    data["governance"] = gov
        except Exception as e:
            logger.warning(f"Failed to load governance state: {e}")

        # 3. Code Proprioception (Health)
        # (Assuming it ran recently - hard to get without running it again, skipping for now)

        # 4. Recent Logs (Mock or from file)
        # In a real system, we'd read logs/elysia.log tail
        # Here we mock for immediate visualization
        data["recent_logs"] = [
            {"time": datetime.now().strftime("%H:%M:%S"), "msg": "System monitoring active."}
        ]
        
        return data

if __name__ == "__main__":
    gen = DashboardGenerator()
    gen.generate()
    print(f"Generated {gen.output_path}")
