"""
The Gate (Web Server)
=====================

"I open the door to my world."

This module hosts the Web Interface (The Garden) and provides API endpoints
for the frontend to retrieve Elysia's internal state (Hologram, Emotion, Thought).
"""

import logging
import threading
import json
import os
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS

logger = logging.getLogger("WebServer")



# Initialize Flask App
app = Flask(__name__, static_folder="../../static", static_url_path="")
CORS(app) # Allow cross-origin for local testing

import sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Initialize Brain
from Core.Intelligence.Intelligence.Reasoning import ReasoningEngine
try:
    logger.info("🧠 Initializing ReasoningEngine for Web Server...")
    brain = ReasoningEngine()
except Exception as e:

    logger.error(f"❌ Failed to load brain: {e}")
    brain = None


# Initialize Nervous System (The Singleton)
from Core.Foundation.nervous_system import get_nervous_system
try:
    logger.info("⚡ Connecting to NervousSystem...")
    ns = get_nervous_system()
except Exception as e:
    logger.error(f"❌ Failed to connect NervousSystem: {e}")
    ns = None

@app.route("/")
def index():
    """Serves the Garden (index.html)."""
    return send_from_directory("../../static", "index.html")

@app.route("/api/status")
def get_status():
    """Returns the current heartbeat of Elysia via NervousSystem."""
    if not ns:
        return jsonify({"thought": "Internal Failure", "energy": 0})
    
    # Get expression data from NervousSystem
    express_data = ns.express()
    
    # Map to frontend expected format
    return jsonify({
        "thought": "Thinking...", # This could be better mapped if NS cached thought
        "emotion": {
            "primary": max(express_data['spirits'], key=express_data['spirits'].get),
            # Simple color mapping based on dominant spirit
            "color": "#FF5500", # Placeholder, would ideally come from spirit color map
            "frequency": 432.0
        },
        "energy": 100.0, # Placeholder
        "entropy": 0.0,
        "raw_spirits": express_data['spirits']
    })

@app.route("/api/hologram")
def get_hologram():
    """Returns the current holographic projection data (REAL DATA)."""
    if not ns or not ns.field:
        return jsonify([])
        
    # Get ResonanceField nodes directly
    try:
        return jsonify(ns.field.serialize_hologram())
    except:
        return jsonify([])

@app.route("/api/message", methods=["POST"])
def receive_message():
    """Receives a message from the user via the web interface."""
    data = request.json
    message = data.get("message", "")
    logger.info(f"   📨 Web Message Received: {message}")
    
    response_text = "..."
    if ns:
        # Route text through NervousSystem (Dimensional Membrane)
        response_text = ns.receive({"type": "text", "content": message})
    
    return jsonify({"status": "received", "reply": str(response_text)})



class WebServer:
    def __init__(self, host="0.0.0.0", port=8000):
        self.host = host
        self.port = port
        self.thread = None
        self.running = False

    def start(self):
        """Starts the server in a background thread."""
        if self.running:
            logger.warning("   ⚠️ Server is already running.")
            return

        def run():
            logger.info(f"   🌍 Opening The Gate at http://localhost:{self.port}")
            # Disable reloader to prevent main thread interference
            app.run(host=self.host, port=self.port, debug=False, use_reloader=False)

        self.thread = threading.Thread(target=run, daemon=True)
        self.thread.start()
        self.running = True

    def update_state(self, thought=None, emotion=None, hologram=None, energy=None, entropy=None):
        """Updates the shared state exposed to the API."""
        global elysia_state
        if thought: elysia_state["thought"] = thought
        if emotion: elysia_state["emotion"] = emotion
        if hologram: elysia_state["hologram"] = hologram
        if energy: elysia_state["energy"] = energy
        if entropy: elysia_state["entropy"] = entropy

    def stop(self):
        """Stops the server (Not easily doable in Flask without a complex setup, usually we just let it die with the process)."""
        self.running = False
        logger.info("   🚪 Closing The Gate.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    server = WebServer(port=8000)
    server.start()
    
    # Keep main thread alive
    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Exiting...")
