"""
Unified Monitor for Elysia v9.0
===============================
Merges `system_monitor` (Hardware) and `performance_monitor` (Software Profiling).
One Organ to track the Body (Hardware) and the Mind (Software).
"""

import time
import psutil
import logging
import os
import functools
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable
from elysia_core import Cell, Organ

logger = logging.getLogger("UnifiedMonitor")

@dataclass
class SystemMetrics:
    """Hardware Health Snapshot"""
    timestamp: float
    cpu_usage: float
    memory_usage: float
    disk_free_mb: float
    
@dataclass
class PerformanceMetric:
    """Software Execution Snapshot"""
    operation: str
    duration_ms: float
    memory_delta_mb: float
    timestamp: float

@Cell("UnifiedMonitor")
class UnifiedMonitor:
    def __init__(self):
        self.metrics_history: List[SystemMetrics] = []
        self.perf_history: List[PerformanceMetric] = []
        self.start_time = time.time()
        self._process = psutil.Process()
        
        # Thresholds
        self.thresholds: Dict[str, float] = {}
        logger.info("🛡️ UnifiedMonitor Initialized (Body & Mind Tracking)")

    # --- PART 1: Hardware Monitoring (The Body) ---
    
    def check_health(self) -> Dict[str, bool]:
        """Returns True if hardware is safe to operate."""
        metrics = self.collect_system_metrics()
        
        safe = True
        reasons = []
        
        if metrics.cpu_usage > 85.0:
            safe = False
            reasons.append(f"CPU Hot ({metrics.cpu_usage}%)")
            
        if metrics.memory_usage > 90.0:
            safe = False
            reasons.append(f"Memory Full ({metrics.memory_usage}%)")
            
        return {
            "safe": safe,
            "reason": ", ".join(reasons),
            "metrics": metrics
        }

    def collect_system_metrics(self) -> SystemMetrics:
        try:
            cpu = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory().percent
            disk = psutil.disk_usage(os.getcwd()).free / (1024 * 1024)
        except:
            # Fallback
            cpu, mem, disk = 10.0, 20.0, 5000.0
            
        metrics = SystemMetrics(time.time(), cpu, mem, disk)
        self.metrics_history.append(metrics)
        if len(self.metrics_history) > 100:
            self.metrics_history.pop(0)
        return metrics

    # --- PART 2: Performance Monitoring (The Mind) ---

    def measure(self, operation: str = None) -> Callable:
        """Decorator to measure function performance."""
        def decorator(func: Callable) -> Callable:
            op_name = operation or func.__name__
            
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_t = time.perf_counter()
                start_m = self._process.memory_info().rss / 1024 / 1024
                
                try:
                    return func(*args, **kwargs)
                finally:
                    end_t = time.perf_counter()
                    end_m = self._process.memory_info().rss / 1024 / 1024
                    
                    duration = (end_t - start_t) * 1000
                    mem_delta = end_m - start_m
                    
                    self._record_perf(op_name, duration, mem_delta)
            return wrapper
        return decorator

    def _record_perf(self, op: str, duration: float, mem: float):
        metric = PerformanceMetric(op, duration, mem, time.time())
        self.perf_history.append(metric)
        
        # Log slow operations (Simulating Pain)
        threshold = self.thresholds.get(op, 1000.0)
        if duration > threshold:
            logger.warning(f"⚠️ Slow Thought: '{op}' took {duration:.2f}ms")

# Global Access via Organ (Implicitly handled by @Cell)
