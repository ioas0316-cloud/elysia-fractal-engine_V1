import psutil
import time
from .intelligence_line import IntelligenceLine, LineOutput

class KinestheticLine(IntelligenceLine):
    """
    Kinesthetic Line (운동신경 지능)
    Monitors the "Physical Body" of the AI (CPU, RAM, System Time).
    """

    def __init__(self, mock_load: float = None):
        """
        Args:
            mock_load: If set, overrides the actual system sensor for testing. 0.0 to 1.0.
        """
        self.name = "Kinesthetic"
        self.mock_load = mock_load

    def perceive(self, context_input: any = None) -> LineOutput:

        if self.mock_load is not None:
             signal = self.mock_load
             cpu_percent = signal * 100
             memory_percent = signal * 100
        else:
            # 1. Measure CPU Usage
            cpu_percent = psutil.cpu_percent(interval=None) # Non-blocking for speed

            # 2. Measure Memory Usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent

            # 3. Determine State
            # Normalized signal: 0.0 (Idle) -> 1.0 (Overloaded)
            # We take the max of CPU or RAM stress
            signal = max(cpu_percent / 100.0, memory_percent / 100.0)

        description = "Normal"
        if signal > 0.8:
            description = "Feverish (High Load)"
        elif signal > 0.5:
            description = "Active (Moderate Load)"
        else:
            description = "Calm (Idle)"

        return LineOutput(
            source="Kinesthetic",
            signal=signal,
            description=f"Body is {description} (CPU: {cpu_percent:.1f}%, MEM: {memory_percent:.1f}%)",
            raw_data={
                "cpu": cpu_percent,
                "memory": memory_percent,
                "timestamp": time.time()
            }
        )
