from typing import Optional, Dict, Any

from dataclasses import dataclass

from datetime import datetime

from Core.Foundation.emotional_state import EmotionalState



@dataclass

class Memory:

    timestamp: str

    content: str

    emotional_state: Optional[EmotionalState] = None

    context: Optional[Dict[str, Any]] = None

    value_alignment: Optional[float] = None



class CoreMemoryBase:

    def __init__(self, data: Dict[str, Any]):

        self.data = data or {

            'identity': {},

            'values': [],

            'experiences': [],

            'relationships': {},

            'rules': []

        }

        

    def get_identity(self) -> Dict[str, Any]:

        return self.data.get('identity', {})

        

    def get_values(self) -> list:

        return self.data.get('values', [])

        

    def get_experiences(self, n: Optional[int] = None) -> list:

        experiences = self.data.get('experiences', [])

        if n:

            return experiences[-n:]

        return experiences

        

    def get_relationship(self, person: str) -> Optional[Dict[str, Any]]:

        return self.data.get('relationships', {}).get(person)

        

    def get_rules(self) -> list:

        return self.data.get('rules', [])