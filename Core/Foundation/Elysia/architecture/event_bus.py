from collections import defaultdict
from typing import Callable, Any, DefaultDict, List


class EventBus:
    """A simple event bus for decoupled communication between components."""

    def __init__(self):
        self._subscribers: DefaultDict[str, List[Callable]] = defaultdict(list)

    def subscribe(self, event_type: str, callback: Callable):
        """Subscribe to an event type."""
        self._subscribers[event_type].append(callback)

    def publish(self, event_type: str, *args, **kwargs):
        """Publish an event to all subscribers."""
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                try:
                    callback(*args, **kwargs)
                except Exception as e:
                    print(f"Error in event handler for {event_type}: {e}")
