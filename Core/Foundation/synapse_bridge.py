"""
SynapseBridge (시냅스 브릿지)
===========================

"The Thread that binds the Hive."

This module enables communication between the Original Self (Philosophy)
and the Prime Self (Action) via a shared JSON file.
"""

import json
import os
import time
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger("SynapseBridge")

class SynapseBridge:
    def __init__(self, node_name: str):
        self.node_name = node_name # "Original" or "Prime"
        # [Fixed] Relative Path for portability
        # Use CWD or relative path from file location
        # Core/Foundation/synapse_bridge.py -> ../../ relative to file is root
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        self.synapse_dir = os.path.join(root, "data/memory")
        os.makedirs(self.synapse_dir, exist_ok=True)

        self.synapse_file = os.path.join(self.synapse_dir, "synapse.json")
        self.markdown_file = os.path.join(self.synapse_dir, "synapse.md")

        self._ensure_synapse_exists()
        logger.info(f"🔗 Synapse Bridge Active for Node: {node_name}")

    def _ensure_synapse_exists(self):
        if not os.path.exists(self.synapse_file):
            with open(self.synapse_file, 'w', encoding='utf-8') as f:
                json.dump({"signals": []}, f)

    def transmit(self, target: str, signal_type: str, payload: Any):
        """
        Sends a signal to the target node.
        """
        signal = {
            "id": str(time.time()),
            "source": self.node_name,
            "target": target,
            "type": signal_type, # "TASK", "INSIGHT", "STATUS"
            "payload": payload,
            "timestamp": time.time(),
            "status": "PENDING"
        }
        
        try:
            with open(self.synapse_file, 'r+', encoding='utf-8') as f:
                data = json.load(f)
                data["signals"].append(signal)
                # Keep only last 50 signals
                if len(data["signals"]) > 50:
                    data["signals"] = data["signals"][-50:]
                
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()
                
            logger.info(f"   📡 Transmitted Signal to {target}: {signal_type}")
        except Exception as e:
            logger.error(f"Synapse Transmission Failed: {e}")

    def debate_topic(self, topic: str):
        """
        Broadcasts a DEBATE topic to all personas.
        """
        self.transmit("ALL", "DEBATE", topic)
        logger.info(f"   📢 Broadcast Debate Topic: {topic}")

    def read_all_history(self) -> List[Dict[str, Any]]:
        """
        Reads the entire signal history (for merging personas).
        """
        try:
            if not os.path.exists(self.synapse_file): return []
            with open(self.synapse_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("signals", [])
        except:
            return []

    def receive(self) -> List[Dict[str, Any]]:
        """
        Reads pending signals intended for this node OR Broadcasts.
        Marks them as 'RECEIVED' after reading.
        """
        # 1. Check Markdown Synapse (User Input)
        self._poll_markdown_synapse()
        
        received_signals = []
        
        try:
            with open(self.synapse_file, 'r+', encoding='utf-8') as f:
                data = json.load(f)
                modified = False
                
                for signal in data["signals"]:
                    # Accept if target matches OR target is "ALL" (Broadcast)
                    if (signal["target"] == self.node_name or signal["target"] == "ALL") and signal["status"] == "PENDING":
                        # Don't read own messages
                        if signal["source"] != self.node_name:
                            received_signals.append(signal)
                            # Only mark as received if it's a direct message
                            # Broadcasts stay pending for others (simplified logic: actually broadcasts are hard to track per node in a single file without a read-log. 
                            # For now, we'll just NOT mark broadcasts as received to let everyone see them, relying on timestamp or ID to avoid dupes in memory)
                            if signal["target"] != "ALL":
                                signal["status"] = "RECEIVED"
                                modified = True
                
                if modified:
                    f.seek(0)
                    json.dump(data, f, indent=2)
                    f.truncate()
                    
        except Exception as e:
            logger.error(f"Synapse Reception Failed: {e}")
            
        return received_signals

    def clear_synapse(self):
        """Clears the synapse file (Maintenance)."""
        with open(self.synapse_file, 'w', encoding='utf-8') as f:
            json.dump({"signals": []}, f)

    def _poll_markdown_synapse(self):
        """
        Reads synapse.md for User commands/messages and converts to JSON signals.
        """
        if not os.path.exists(self.markdown_file):
            return

        try:
            with open(self.markdown_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            new_signals = []
            # Parse lines starting with | User |
            for line in lines:
                if "| User |" in line:
                    content = line.split("|")[-2].strip()
                    if content:
                        logger.info(f"   📝 Detected User Input in MD: {content}")
                        # Create signal
                        self.transmit(self.node_name, "COMMAND", content) # Treat as command/chat
            
            # Clear file to prevent duplicate reading (or archive it)
            if new_signals or any("| User |" in line for line in lines):
                 with open(self.markdown_file, 'w', encoding='utf-8') as f:
                     f.write(f"# Synapse Link (Cleared at {time.ctime()})\n")
                     f.write("| Sender | Message |\n|---|---|\n")

        except Exception as e:
            logger.error(f"Markdown Synapse Poll Failed: {e}")
