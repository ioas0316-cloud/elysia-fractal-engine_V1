
class DialogueInterface:
    def __init__(self): pass
    def speak(self, input_text, insight):
        # Fallback to simple formatted response
        if hasattr(insight, "content"):
            return str(insight.content)
        return str(insight)
