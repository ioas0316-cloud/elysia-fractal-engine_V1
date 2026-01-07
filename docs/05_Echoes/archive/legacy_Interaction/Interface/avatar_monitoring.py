"""
Avatar Server Monitoring System
================================

실시간 성능 모니터링 시스템 - CPU, 메모리, 네트워크, FPS, 레이턴시

Provides:
- Real-time performance metrics (CPU, memory, network)
- FPS counter for client rendering
- WebSocket latency tracking
- Connected clients statistics
- System health monitoring

Architecture:
    Metrics Collection → Aggregation → Broadcast → Dashboard Display
"""

import logging
import time
import asyncio
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict
from collections import deque
from datetime import datetime

# Optional system metrics (psutil)
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    logging.warning("⚠️ psutil not available - system metrics disabled")

logger = logging.getLogger("AvatarMonitoring")

@dataclass
class SystemMetrics:
    """System-level performance metrics"""
    timestamp: float
    cpu_percent: float  # CPU usage percentage
    memory_percent: float  # Memory usage percentage
    memory_used_mb: float  # Memory used in MB
    memory_total_mb: float  # Total memory in MB
    network_sent_mb: float  # Network bytes sent (MB)
    network_recv_mb: float  # Network bytes received (MB)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class ClientMetrics:
    """Per-client performance metrics"""
    client_id: str
    connected_at: float
    messages_sent: int = 0
    messages_received: int = 0
    bytes_sent: int = 0
    bytes_received: int = 0
    avg_latency_ms: float = 0.0
    last_message_time: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['connection_duration'] = time.time() - self.connected_at
        return data


@dataclass
class ServerMetrics:
    """Server-level metrics"""
    uptime_seconds: float
    total_connections: int
    active_connections: int
    total_messages: int
    messages_per_second: float
    avg_latency_ms: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


class MetricsCollector:
    """
    Collects system and application metrics.
    
    Features:
    - System metrics (CPU, memory, network)
    - Client metrics (connections, messages, latency)
    - Server metrics (uptime, throughput)
    """
    
    def __init__(self):
        """Initialize metrics collector"""
        self.start_time = time.time()
        self.client_metrics: Dict[str, ClientMetrics] = {}
        
        # System metrics history (last 60 samples = 1 minute at 1Hz)
        self.system_metrics_history: deque = deque(maxlen=60)
        
        # Message rate tracking
        self.message_timestamps: deque = deque(maxlen=1000)
        
        # Latency tracking
        self.latency_samples: deque = deque(maxlen=100)
        
        # Network baseline (if psutil available)
        self.network_baseline_sent = 0
        self.network_baseline_recv = 0
        if PSUTIL_AVAILABLE:
            net_io = psutil.net_io_counters()
            self.network_baseline_sent = net_io.bytes_sent
            self.network_baseline_recv = net_io.bytes_recv
        
        logger.info("📊 MetricsCollector initialized")
    
    def collect_system_metrics(self) -> SystemMetrics:
        """
        Collect current system metrics
        
        Returns:
            SystemMetrics object with current values
        """
        # Default values if psutil not available
        cpu_percent = 0.0
        memory_percent = 0.0
        memory_used_mb = 0.0
        memory_total_mb = 0.0
        network_sent_mb = 0.0
        network_recv_mb = 0.0
        
        if PSUTIL_AVAILABLE:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            
            # Memory usage
            mem = psutil.virtual_memory()
            memory_percent = mem.percent
            memory_used_mb = mem.used / (1024 * 1024)
            memory_total_mb = mem.total / (1024 * 1024)
            
            # Network usage (total since baseline)
            net_io = psutil.net_io_counters()
            network_sent_mb = (net_io.bytes_sent - self.network_baseline_sent) / (1024 * 1024)
            network_recv_mb = (net_io.bytes_recv - self.network_baseline_recv) / (1024 * 1024)
        
        metrics = SystemMetrics(
            timestamp=time.time(),
            cpu_percent=cpu_percent,
            memory_percent=memory_percent,
            memory_used_mb=memory_used_mb,
            memory_total_mb=memory_total_mb,
            network_sent_mb=network_sent_mb,
            network_recv_mb=network_recv_mb
        )
        
        # Add to history
        self.system_metrics_history.append(metrics)
        
        return metrics
    
    def register_client(self, client_id: str):
        """Register a new client connection"""
        self.client_metrics[client_id] = ClientMetrics(
            client_id=client_id,
            connected_at=time.time()
        )
        logger.info(f"📈 Registered client for monitoring: {client_id[:16]}...")
    
    def unregister_client(self, client_id: str):
        """Unregister a disconnected client"""
        if client_id in self.client_metrics:
            del self.client_metrics[client_id]
            logger.info(f"📉 Unregistered client from monitoring: {client_id[:16]}...")
    
    def record_message_sent(self, client_id: str, message_size: int):
        """Record a message sent to client"""
        if client_id in self.client_metrics:
            self.client_metrics[client_id].messages_sent += 1
            self.client_metrics[client_id].bytes_sent += message_size
        
        self.message_timestamps.append(time.time())
    
    def record_message_received(self, client_id: str, message_size: int):
        """Record a message received from client"""
        if client_id in self.client_metrics:
            self.client_metrics[client_id].messages_received += 1
            self.client_metrics[client_id].bytes_received += message_size
            self.client_metrics[client_id].last_message_time = time.time()
        
        self.message_timestamps.append(time.time())
    
    def record_latency(self, client_id: str, latency_ms: float):
        """Record message latency"""
        if client_id in self.client_metrics:
            # Update client average (exponential moving average)
            alpha = 0.3
            current_avg = self.client_metrics[client_id].avg_latency_ms
            self.client_metrics[client_id].avg_latency_ms = (
                alpha * latency_ms + (1 - alpha) * current_avg
            )
        
        self.latency_samples.append(latency_ms)
    
    def get_server_metrics(self) -> ServerMetrics:
        """
        Get current server metrics
        
        Returns:
            ServerMetrics object
        """
        uptime = time.time() - self.start_time
        active_connections = len(self.client_metrics)
        
        # Calculate total messages
        total_messages = sum(
            cm.messages_sent + cm.messages_received 
            for cm in self.client_metrics.values()
        )
        
        # Calculate messages per second (last minute)
        now = time.time()
        recent_messages = sum(1 for ts in self.message_timestamps if now - ts < 1.0)
        
        # Calculate average latency
        avg_latency = (
            sum(self.latency_samples) / len(self.latency_samples)
            if self.latency_samples else 0.0
        )
        
        return ServerMetrics(
            uptime_seconds=uptime,
            total_connections=len(self.client_metrics),  # Could track total ever
            active_connections=active_connections,
            total_messages=total_messages,
            messages_per_second=recent_messages,
            avg_latency_ms=avg_latency
        )
    
    def get_all_metrics(self) -> Dict[str, Any]:
        """
        Get all current metrics
        
        Returns:
            Dictionary with system, server, and client metrics
        """
        system_metrics = self.collect_system_metrics()
        server_metrics = self.get_server_metrics()
        
        # Get client metrics
        client_list = [cm.to_dict() for cm in self.client_metrics.values()]
        
        return {
            'timestamp': time.time(),
            'system': system_metrics.to_dict(),
            'server': server_metrics.to_dict(),
            'clients': client_list,
            'history': {
                'system': [m.to_dict() for m in list(self.system_metrics_history)[-10:]]
            }
        }


class PerformanceMonitor:
    """
    Main monitoring system that integrates metrics collection and broadcasting.
    
    Features:
    - Automatic metrics collection
    - Real-time broadcasting to clients
    - Performance alerts
    """
    
    def __init__(self, update_interval: float = 1.0):
        """
        Initialize performance monitor
        
        Args:
            update_interval: How often to collect and broadcast metrics (seconds)
        """
        self.update_interval = update_interval
        self.collector = MetricsCollector()
        self.enabled = True
        self.broadcast_callback = None
        
        logger.info(f"🎯 PerformanceMonitor initialized (interval: {update_interval}s)")
    
    def set_broadcast_callback(self, callback):
        """Set callback function for broadcasting metrics"""
        self.broadcast_callback = callback
    
    async def start_monitoring(self):
        """Start the monitoring loop"""
        logger.info("▶️ Starting monitoring loop")
        
        while self.enabled:
            try:
                # Collect metrics
                metrics = self.collector.get_all_metrics()
                
                # Broadcast to clients if callback is set
                if self.broadcast_callback:
                    await self.broadcast_callback(metrics)
                
                # Check for performance issues
                self._check_performance_alerts(metrics)
                
                # Wait for next update
                await asyncio.sleep(self.update_interval)
            
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(1.0)
        
        logger.info("⏸️ Monitoring loop stopped")
    
    def _check_performance_alerts(self, metrics: Dict[str, Any]):
        """Check for performance issues and log alerts"""
        system = metrics['system']
        
        # CPU alert
        if system['cpu_percent'] > 80:
            logger.warning(f"⚠️ High CPU usage: {system['cpu_percent']:.1f}%")
        
        # Memory alert
        if system['memory_percent'] > 85:
            logger.warning(f"⚠️ High memory usage: {system['memory_percent']:.1f}%")
        
        # Latency alert
        server = metrics['server']
        if server['avg_latency_ms'] > 100:
            logger.warning(f"⚠️ High latency: {server['avg_latency_ms']:.1f}ms")
    
    def stop(self):
        """Stop monitoring"""
        self.enabled = False
        logger.info("🛑 Performance monitor stopped")


class FPSCounter:
    """
    Client-side FPS (Frames Per Second) counter.
    
    Tracks rendering performance on the client side.
    """
    
    def __init__(self, window_size: int = 60):
        """
        Initialize FPS counter
        
        Args:
            window_size: Number of frames to average over
        """
        self.window_size = window_size
        self.frame_times: deque = deque(maxlen=window_size)
        self.last_frame_time = time.time()
    
    def record_frame(self) -> float:
        """
        Record a new frame and return current FPS
        
        Returns:
            Current FPS value
        """
        now = time.time()
        delta = now - self.last_frame_time
        self.last_frame_time = now
        
        self.frame_times.append(delta)
        
        # Calculate FPS
        if len(self.frame_times) > 0:
            avg_delta = sum(self.frame_times) / len(self.frame_times)
            fps = 1.0 / avg_delta if avg_delta > 0 else 0.0
            return fps
        
        return 0.0
    
    def get_stats(self) -> Dict[str, float]:
        """Get FPS statistics"""
        if not self.frame_times:
            return {'fps': 0.0, 'frame_time_ms': 0.0}
        
        avg_delta = sum(self.frame_times) / len(self.frame_times)
        fps = 1.0 / avg_delta if avg_delta > 0 else 0.0
        
        return {
            'fps': fps,
            'frame_time_ms': avg_delta * 1000,
            'samples': len(self.frame_times)
        }


# Factory functions
def create_performance_monitor(update_interval: float = 1.0) -> PerformanceMonitor:
    """
    Create PerformanceMonitor instance
    
    Args:
        update_interval: Metrics update interval in seconds
        
    Returns:
        Configured PerformanceMonitor
    """
    return PerformanceMonitor(update_interval=update_interval)


def create_fps_counter(window_size: int = 60) -> FPSCounter:
    """
    Create FPSCounter instance
    
    Args:
        window_size: Number of frames to average
        
    Returns:
        Configured FPSCounter
    """
    return FPSCounter(window_size=window_size)
