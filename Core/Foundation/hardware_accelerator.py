import logging

# [Lazy Load] Torch is optional
_torch = None
def _get_torch():
    global _torch
    if _torch is None:
        try:
            import torch
            _torch = torch
        except ImportError:
            _torch = False
    return _torch if _torch else None

class HardwareAccelerator:
    """
    Manages hardware acceleration resources (CPU/GPU).
    Detects CUDA availability and provides methods to utilize the best available device.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        torch = _get_torch()
        if not torch:
            self.device = None
            self.logger.warning("Hardware Accelerator: PyTorch unavailable, running in degraded mode")
            return
            
        self.device = self._detect_device()
        self.logger.info(f"Hardware Accelerator initialized on: {self.device}")
        if self.device.type == 'cuda':
            self.logger.info(f"GPU Name: {torch.cuda.get_device_name(0)}")
            self._log_memory_stats()

    def _detect_device(self):
        """
        Detects if CUDA is available and returns the appropriate torch device.
        """
        torch = _get_torch()
        if not torch:
            return None
        if torch.cuda.is_available():
            return torch.device("cuda")
        else:
            return torch.device("cpu")

    def get_device(self):
        """
        Returns the currently active torch device.
        """
        return self.device

    def tensor(self, data, dtype=None):
        """
        Creates a tensor on the active device.
        """
        torch = _get_torch()
        if not torch or not self.device:
            return None
        return torch.tensor(data, device=self.device, dtype=dtype)

    def to_device(self, tensor):
        """
        Moves a tensor to the active device.
        """
        if not self.device or tensor is None:
            return tensor
        return tensor.to(self.device)

    def get_memory_stats(self) -> dict:
        """
        Returns memory statistics for the current device.
        Returns empty dict if on CPU.
        """
        torch = _get_torch()
        stats = {}
        if torch and self.device and self.device.type == 'cuda':
            stats['allocated'] = torch.cuda.memory_allocated(0)
            stats['reserved'] = torch.cuda.memory_reserved(0)
            stats['max_allocated'] = torch.cuda.max_memory_allocated(0)
        return stats

    def _log_memory_stats(self):
        """
        Logs current memory statistics.
        """
        if self.device and self.device.type == 'cuda':
            stats = self.get_memory_stats()
            self.logger.info(
                f"VRAM Stats - Allocated: {stats['allocated'] / 1024**2:.2f} MB, "
                f"Reserved: {stats['reserved'] / 1024**2:.2f} MB"
            )

# [Lazy Load] Global instance - created on first access
_accelerator = None
def get_accelerator():
    global _accelerator
    if _accelerator is None:
        _accelerator = HardwareAccelerator()
    return _accelerator

# Legacy compatibility (but now lazy)
accelerator = None  # Will be set on first use
def _init_accelerator():
    global accelerator
    if accelerator is None:
        accelerator = get_accelerator()
    return accelerator
