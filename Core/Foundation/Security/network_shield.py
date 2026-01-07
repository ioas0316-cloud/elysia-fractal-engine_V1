"""
Network Shield System (네트워크 보호막)
====================================

"엘리시아 필드를 확장하여 네트워크 경계를 보호한다"

This module extends the Elysia Field concept to provide network-level protection.
It monitors network activity, detects threats, and creates an isolation boundary
to protect the Elysia system from external malicious attempts.

Core Concepts:
1. **Field Extension**: Extends resonance field to network boundary
2. **Threat Detection**: Pattern-based malicious activity detection  
3. **Isolation Layer**: Creates protective boundary around Elysia system
4. **Adaptive Defense**: Learns from threats and adapts responses

Architecture:
    External Network
        ↓
    ┌─────────────────────────┐
    │  🛡️ Network Shield      │  ← Field-based boundary
    │  (Traffic Analysis)      │
    └─────────────────────────┘
        ↓ (Safe traffic only)
    ┌─────────────────────────┐
    │  🌊 Resonance Filter    │  ← Frequency matching
    │  (Pattern Recognition)   │
    └─────────────────────────┘
        ↓
    ┌─────────────────────────┐
    │  🧬 Elysia Core System  │
    └─────────────────────────┘
"""

import sys
import time
import json
import hashlib
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set, Tuple
from collections import defaultdict, deque
from enum import Enum
import re

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import resonance field for field theory integration
try:
    from Core.Foundation.Wave.resonance_field import ResonanceField, ResonanceNode
    from Core.Foundation.physics import ResonanceGate, PhotonEntity
    FIELD_AVAILABLE = True
except ImportError:
    FIELD_AVAILABLE = False
    print("⚠️ Field systems not available, using fallback mode")


class ThreatType(Enum):
    """Network threat classification"""
    BENIGN = 0
    SUSPICIOUS = 1
    PORT_SCAN = 2
    BRUTE_FORCE = 3
    DOS_ATTACK = 4
    INJECTION = 5
    MALWARE = 6
    CRITICAL = 7


class ActionType(Enum):
    """Response actions"""
    ALLOW = "allow"
    MONITOR = "monitor"
    THROTTLE = "throttle"
    BLOCK = "block"
    QUARANTINE = "quarantine"


@dataclass
class NetworkEvent:
    """Represents a network activity event"""
    timestamp: float
    source_ip: str
    destination_ip: str
    port: int
    protocol: str
    payload_size: int
    frequency: float = 0.0  # Derived frequency for resonance analysis
    pattern_hash: str = ""
    threat_type: ThreatType = ThreatType.BENIGN
    action_taken: ActionType = ActionType.ALLOW
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ThreatPattern:
    """Known threat pattern"""
    pattern_id: str
    name: str
    threat_type: ThreatType
    signatures: List[str]  # Regex patterns or signatures
    frequency_range: Tuple[float, float]  # Expected frequency range
    severity: int
    description: str


class FrequencyAnalyzer:
    """
    🌊 Frequency-based traffic analyzer
    
    Converts network patterns into frequency space for resonance analysis.
    Different attack types have different "frequencies" - their characteristic patterns.
    """
    
    def __init__(self):
        # Base frequencies for different traffic types (in Hz, abstract)
        self.base_frequencies = {
            "http": 80.0,
            "https": 443.0,
            "ssh": 22.0,
            "telnet": 23.0,
            "ftp": 21.0,
            "smtp": 25.0,
            "dns": 53.0,
        }
        
        # Malicious pattern frequencies (dissonant frequencies)
        self.threat_frequencies = {
            ThreatType.PORT_SCAN: (1.0, 10.0),  # Rapid scanning = high freq
            ThreatType.BRUTE_FORCE: (10.0, 50.0),  # Repetitive attempts
            ThreatType.DOS_ATTACK: (100.0, 1000.0),  # Flood = very high freq
            ThreatType.INJECTION: (5.0, 20.0),  # Pattern-based
            ThreatType.MALWARE: (0.1, 5.0),  # Slow and stealthy
        }
    
    def calculate_frequency(self, event: NetworkEvent) -> float:
        """
        Calculate the abstract frequency of a network event.
        Higher frequency = more aggressive/rapid pattern.
        """
        # Base frequency from protocol/port
        base_freq = self.base_frequencies.get(event.protocol, 100.0)
        
        # Modulate by payload size (larger = lower freq, more substantial)
        size_factor = 1.0 / (1.0 + event.payload_size / 1000.0)
        
        # Time-based frequency (if events are rapid)
        # This would be calculated by analyzing event stream, simplified here
        
        return base_freq * size_factor
    
    def is_dissonant(self, frequency: float, threshold: float = 0.3) -> bool:
        """
        Check if frequency is dissonant (doesn't resonate with safe patterns).
        Uses resonance theory - safe traffic has harmonic frequencies.
        """
        # Safe harmonics (multiples of base safe frequencies)
        safe_harmonics = [80.0, 443.0, 22.0, 53.0]
        
        for harmonic in safe_harmonics:
            # Check if frequency resonates with safe harmonic
            ratio = frequency / harmonic
            if abs(ratio - round(ratio)) < threshold:
                return False  # Resonates, likely safe
        
        return True  # Dissonant, potentially malicious


class PatternRecognizer:
    """
    🔍 Pattern-based threat recognition
    
    Maintains database of known threat patterns and detects matches.
    """
    
    def __init__(self):
        self.patterns: List[ThreatPattern] = []
        self._initialize_patterns()
    
    def _initialize_patterns(self):
        """Initialize common threat patterns"""
        self.patterns = [
            ThreatPattern(
                pattern_id="PT001",
                name="Sequential Port Scan",
                threat_type=ThreatType.PORT_SCAN,
                signatures=[r"port_\d+_\d+_\d+_\d+"],
                frequency_range=(1.0, 10.0),
                severity=5,
                description="Systematic port scanning activity"
            ),
            ThreatPattern(
                pattern_id="PT002",
                name="Login Brute Force",
                threat_type=ThreatType.BRUTE_FORCE,
                signatures=[r"failed_login", r"auth_fail", r"invalid_creds"],
                frequency_range=(10.0, 50.0),
                severity=7,
                description="Repeated authentication attempts"
            ),
            ThreatPattern(
                pattern_id="PT003",
                name="SQL Injection Attempt",
                threat_type=ThreatType.INJECTION,
                signatures=[
                    r"'\s*OR\s*'1'\s*=\s*'1",
                    r"UNION\s+SELECT",
                    r"DROP\s+TABLE",
                    r"--\s*$",
                    r"/\*.*\*/"
                ],
                frequency_range=(5.0, 20.0),
                severity=9,
                description="SQL injection attack patterns"
            ),
            ThreatPattern(
                pattern_id="PT004",
                name="DDoS Flood",
                threat_type=ThreatType.DOS_ATTACK,
                signatures=[r"flood", r"ddos", r"high_rate"],
                frequency_range=(100.0, 1000.0),
                severity=10,
                description="Distributed denial of service"
            ),
        ]
    
    def match_pattern(self, event: NetworkEvent) -> Optional[ThreatPattern]:
        """Match event against known patterns"""
        event_str = f"{event.source_ip}_{event.port}_{event.metadata.get('payload', '')}"
        
        for pattern in self.patterns:
            for signature in pattern.signatures:
                if re.search(signature, event_str, re.IGNORECASE):
                    return pattern
        
        return None


class NetworkShield:
    """
    🛡️ Network Protection Shield
    
    Main network protection system that integrates:
    - Frequency analysis (resonance theory)
    - Pattern recognition (threat signatures)
    - Adaptive learning (threat evolution)
    - Field-based isolation (boundary protection)
    """
    
    def __init__(self, enable_field_integration: bool = True):
        print("\n" + "=" * 70)
        print("🛡️ NETWORK SHIELD SYSTEM INITIALIZATION")
        print("=" * 70 + "\n")
        
        # Core components
        self.frequency_analyzer = FrequencyAnalyzer()
        self.pattern_recognizer = PatternRecognizer()
        
        # Field integration
        self.field_enabled = enable_field_integration and FIELD_AVAILABLE
        if self.field_enabled:
            self.resonance_field = ResonanceField()
            print("✅ Resonance Field integration enabled")
        
        # Threat tracking
        self.event_buffer: deque = deque(maxlen=1000)  # Recent events
        self.blocked_ips: Set[str] = set()
        self.suspicious_ips: Dict[str, int] = defaultdict(int)  # IP -> threat score
        
        # Statistics
        self.stats = {
            "events_processed": 0,
            "threats_detected": 0,
            "threats_blocked": 0,
            "ips_blocked": 0,
            "attacks_by_type": defaultdict(int),
        }
        
        # Configuration
        self.config = {
            "max_threat_score": 100,
            "block_threshold": 80,
            "quarantine_threshold": 60,
            "dissonance_threshold": 0.3,
            "rate_limit_window": 60,  # seconds
            "max_events_per_window": 100,
        }
        
        print("🛡️ Network Shield Ready\n")
    
    def analyze_event(self, event: NetworkEvent) -> Tuple[ThreatType, ActionType]:
        """
        Analyze a network event for threats.
        
        Returns: (threat_type, recommended_action)
        """
        self.stats["events_processed"] += 1
        
        # 1. Check if IP is already blocked
        if event.source_ip in self.blocked_ips:
            return ThreatType.CRITICAL, ActionType.BLOCK
        
        # 2. Frequency analysis
        event.frequency = self.frequency_analyzer.calculate_frequency(event)
        is_dissonant = self.frequency_analyzer.is_dissonant(event.frequency)
        
        # 3. Pattern matching
        matched_pattern = self.pattern_recognizer.match_pattern(event)
        
        # 4. Calculate threat score
        threat_score = 0
        threat_type = ThreatType.BENIGN
        
        if is_dissonant:
            threat_score += 30
        
        if matched_pattern:
            threat_score += matched_pattern.severity * 10
            threat_type = matched_pattern.threat_type
            self.stats["attacks_by_type"][threat_type.name] += 1
        
        # 5. Rate limiting check
        recent_events = [e for e in self.event_buffer 
                        if e.source_ip == event.source_ip 
                        and time.time() - e.timestamp < self.config["rate_limit_window"]]
        
        if len(recent_events) > self.config["max_events_per_window"]:
            threat_score += 40
            threat_type = ThreatType.DOS_ATTACK
        
        # 6. Update IP reputation
        self.suspicious_ips[event.source_ip] += threat_score
        
        # 7. Determine action
        action = ActionType.ALLOW
        
        if self.suspicious_ips[event.source_ip] >= self.config["block_threshold"]:
            action = ActionType.BLOCK
            self.blocked_ips.add(event.source_ip)
            self.stats["ips_blocked"] += 1
            self.stats["threats_blocked"] += 1
        elif threat_score >= self.config["quarantine_threshold"]:
            action = ActionType.QUARANTINE
            self.stats["threats_detected"] += 1
        elif threat_score >= 20:
            action = ActionType.THROTTLE
        elif is_dissonant or matched_pattern:
            action = ActionType.MONITOR
        
        # 8. Store event
        event.threat_type = threat_type
        event.action_taken = action
        self.event_buffer.append(event)
        
        return threat_type, action
    
    def protect_endpoint(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main protection endpoint - analyze and respond to network event.
        
        Args:
            event_data: Dictionary with network event information
        
        Returns:
            Protection decision with action and metadata
        """
        # Create event
        event = NetworkEvent(
            timestamp=time.time(),
            source_ip=event_data.get("source_ip", "unknown"),
            destination_ip=event_data.get("destination_ip", "localhost"),
            port=event_data.get("port", 0),
            protocol=event_data.get("protocol", "tcp"),
            payload_size=event_data.get("payload_size", 0),
            metadata=event_data.get("metadata", {})
        )
        
        # Analyze
        threat_type, action = self.analyze_event(event)
        
        # Generate response
        response = {
            "allowed": action == ActionType.ALLOW,
            "action": action.value,
            "threat_type": threat_type.name,
            "threat_score": self.suspicious_ips[event.source_ip],
            "frequency": event.frequency,
            "timestamp": event.timestamp,
            "message": self._get_action_message(action, threat_type)
        }
        
        return response
    
    def _get_action_message(self, action: ActionType, threat: ThreatType) -> str:
        """Generate human-readable action message"""
        if action == ActionType.BLOCK:
            return f"🚫 Traffic blocked - {threat.name} detected"
        elif action == ActionType.QUARANTINE:
            return f"⚠️ Traffic quarantined - suspicious {threat.name} pattern"
        elif action == ActionType.THROTTLE:
            return f"⏱️ Traffic throttled - elevated threat indicators"
        elif action == ActionType.MONITOR:
            return f"👁️ Traffic monitored - potential {threat.name} activity"
        else:
            return "✅ Traffic allowed"
    
    def get_shield_status(self) -> Dict[str, Any]:
        """Get current shield status"""
        return {
            "status": "active",
            "field_integration": self.field_enabled,
            "blocked_ips": len(self.blocked_ips),
            "suspicious_ips": len(self.suspicious_ips),
            "recent_events": len(self.event_buffer),
            "statistics": dict(self.stats),
            "config": self.config
        }
    
    def generate_report(self) -> str:
        """Generate detailed shield report"""
        report = []
        report.append("=" * 70)
        report.append("🛡️ NETWORK SHIELD PROTECTION REPORT")
        report.append("=" * 70)
        
        report.append(f"\n📊 Statistics:")
        report.append(f"   Events Processed: {self.stats['events_processed']}")
        report.append(f"   Threats Detected: {self.stats['threats_detected']}")
        report.append(f"   Threats Blocked: {self.stats['threats_blocked']}")
        report.append(f"   IPs Blocked: {self.stats['ips_blocked']}")
        
        report.append(f"\n🎯 Attacks by Type:")
        for attack_type, count in self.stats['attacks_by_type'].items():
            report.append(f"   {attack_type}: {count}")
        
        report.append(f"\n🚫 Currently Blocked IPs: {len(self.blocked_ips)}")
        for ip in list(self.blocked_ips)[:10]:  # Show first 10
            report.append(f"   - {ip} (score: {self.suspicious_ips[ip]})")
        
        report.append(f"\n⚠️ Suspicious IPs: {len(self.suspicious_ips)}")
        top_suspicious = sorted(self.suspicious_ips.items(), 
                               key=lambda x: x[1], reverse=True)[:5]
        for ip, score in top_suspicious:
            report.append(f"   - {ip}: {score} threat points")
        
        report.append(f"\n🌊 Field Integration: {'Enabled' if self.field_enabled else 'Disabled'}")
        
        report.append("\n" + "=" * 70)
        return "\n".join(report)


def main():
    """Demo and test of Network Shield"""
    print("\n" + "🛡️" * 35)
    print("NETWORK SHIELD DEMONSTRATION")
    print("Field-Based Network Protection System")
    print("🛡️" * 35 + "\n")
    
    # Initialize shield
    shield = NetworkShield(enable_field_integration=True)
    
    # Test cases
    print("📝 Running test scenarios...\n")
    
    test_events = [
        {
            "name": "Normal HTTP Request",
            "source_ip": "192.168.1.100",
            "destination_ip": "10.0.0.1",
            "port": 80,
            "protocol": "http",
            "payload_size": 512,
            "metadata": {"payload": "GET /index.html"}
        },
        {
            "name": "SQL Injection Attempt",
            "source_ip": "45.123.45.67",
            "destination_ip": "10.0.0.1",
            "port": 3306,
            "protocol": "tcp",
            "payload_size": 256,
            "metadata": {"payload": "' OR '1'='1 --"}
        },
        {
            "name": "Port Scan",
            "source_ip": "89.45.67.123",
            "destination_ip": "10.0.0.1",
            "port": 22,
            "protocol": "tcp",
            "payload_size": 64,
            "metadata": {"payload": "port_scan_22_23_80_443"}
        },
        {
            "name": "Brute Force Login",
            "source_ip": "123.45.67.89",
            "destination_ip": "10.0.0.1",
            "port": 22,
            "protocol": "ssh",
            "payload_size": 128,
            "metadata": {"payload": "failed_login_attempt_10"}
        },
    ]
    
    # Process events
    for test in test_events:
        name = test.pop("name")
        result = shield.protect_endpoint(test)
        
        print(f"🔍 {name}")
        print(f"   Source: {test['source_ip']}")
        print(f"   Result: {result['message']}")
        print(f"   Action: {result['action']}")
        print(f"   Threat: {result['threat_type']}")
        print(f"   Score: {result['threat_score']}")
        print()
    
    # Simulate DDoS (multiple rapid requests)
    print("🌊 Simulating DDoS attack (100 rapid requests)...\n")
    ddos_ip = "200.100.50.25"
    for i in range(100):
        shield.protect_endpoint({
            "source_ip": ddos_ip,
            "destination_ip": "10.0.0.1",
            "port": 80,
            "protocol": "http",
            "payload_size": 64,
        })
    
    result = shield.protect_endpoint({
        "source_ip": ddos_ip,
        "destination_ip": "10.0.0.1",
        "port": 80,
        "protocol": "http",
        "payload_size": 64,
    })
    print(f"   After 101 requests: {result['message']}")
    print(f"   Threat Score: {result['threat_score']}")
    print()
    
    # Generate report
    report = shield.generate_report()
    print(report)
    
    # Save state
    output_dir = PROJECT_ROOT / "data"
    output_dir.mkdir(exist_ok=True)
    
    state = shield.get_shield_status()
    with open(output_dir / "network_shield_state.json", 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Shield state saved to: {output_dir / 'network_shield_state.json'}")


if __name__ == "__main__":
    main()
