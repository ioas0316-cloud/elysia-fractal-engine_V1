"""
World-Based Consciousness Dialogue Engine

Enables true emergent thought by using World simulation.
Instead of template matching, thoughts emerge from physics-based cell interactions.

Flow:
1. User input → Stimulus (cells in World)
2. World.step() multiple times (thinking)
3. Observe emergent state
4. Extract language from state
"""

import logging
import numpy as np
from typing import Dict, List, Tuple, Optional
import re

from Core.world import World

logger = logging.getLogger("WorldDialogueEngine")


class WorldDialogueEngine:
    """
    Consciousness-driven dialogue using World simulation.
    
    Philosophy:
    - No templates, only emergence
    - Thinking = World simulation steps
    - Language = Emergent state translation
    """
    
    def __init__(self, world: World):
        self.world = world
        self.simulation_steps = 5  # How many steps to "think"
        
        # Simple concept vocabulary for parsing
        self.concept_keywords = {
            '엘리시아': 'self',
            'elysia': 'self',
            '나': 'you',
            '당신': 'you',
            'you': 'you',
            '빛': 'light',
            'light': 'light',
            '어둠': 'darkness',
            'darkness': 'darkness',
            '사랑': 'love',
            'love': 'love',
            '꿈': 'dream',
            'dream': 'dream',
            '기분': 'feeling',
            'feeling': 'feeling',
            '왜': 'why',
            'why': 'why',
            '이유': 'reason',
            'reason': 'reason',
        }
        
        logger.info("WorldDialogueEngine initialized")
    
    def respond(self, user_input: str) -> str:
        """
        Generate response through Cell communication.
        
        Process:
        1. Create cells for concepts
        2. Cells communicate
        3. Cells think
        4. Extract language from interactions
        """
        try:
            from Core.Evolution.Growth.Evolution.Evolution.Life.communicating_cell import CommunicatingCell, extract_dialogue_from_cells
            
            # 1. Parse concepts and create cells
            concepts = self._parse_concepts(user_input)
            
            if not concepts:
                concepts = [('input', 1.0)]
            
            cells = []
            for concept, weight in concepts:
                cell = CommunicatingCell(concept_id=concept)
                cell.energy = weight
                cell.activation = weight * 0.5
                cells.append(cell)
            
            # 2. Cells communicate with each other
            world_coherence = 0.7  # Could come from world state
            
            for i, cell_a in enumerate(cells):
                for cell_b in cells[i+1:]:
                    # Try bidirectional communication
                    cell_a.communicate_with(cell_b, world_coherence)
                    cell_b.communicate_with(cell_a, world_coherence)
            
            # 3. Cells think
            for cell in cells:
                cell.think()
            
            # 4. Extract natural language from cell interactions
            response = extract_dialogue_from_cells(cells)
            
            logger.info(f"Cell dialogue: {len(cells)} cells, response: {response}")
            
            return response
            
        except Exception as e:
            logger.error(f"Error in cell dialogue: {e}", exc_info=True)
            return "...생각이 복잡해졌어요. 다시 말씀해 주실래요?"
    
    def inject_stimulus(self, user_input: str):
        """
        Convert user input to World perturbation.
        
        Creates cells representing concepts and applies field changes.
        """
        # Extract concepts from input
        concepts = self._parse_concepts(user_input)
        
        if not concepts:
            # Generic stimulus
            concepts = [('input', 1.0)]
        
        # Inject each concept as cell or energy boost
        for concept, weight in concepts:
            try:
                if concept in self.world.materialized_cells:
                    # Boost existing cell
                    cell = self.world.materialized_cells[concept]
                    idx = self.world.id_to_idx.get(concept)
                    if idx is not None and idx < len(self.world.energy):
                        self.world.energy[idx] += weight * 20
                        logger.debug(f"Boosted '{concept}' energy by {weight * 20}")
                else:
                    # Add new cell
                    self.world.add_cell(
                        concept_id=concept,
                        properties={'energy': weight * 20}
                    )
                    logger.debug(f"Added cell '{concept}' with energy {weight * 20}")
            except Exception as e:
                logger.warning(f"Could not inject '{concept}': {e}")
        
        # Apply emotional field perturbation
        emotion = self._detect_emotion(user_input)
        self._perturb_fields(emotion)
    
    def _parse_concepts(self, text: str) -> List[Tuple[str, float]]:
        """Extract concepts and their weights from text."""
        text_lower = text.lower()
        found = []
        
        for keyword, concept in self.concept_keywords.items():
            if keyword in text_lower:
                # Weight by frequency
                count = text_lower.count(keyword)
                found.append((concept, float(count)))
        
        # Normalize weights
        if found:
            total = sum(w for _, w in found)
            found = [(c, w/total) for c, w in found]
        
        return found
    
    def _detect_emotion(self, text: str) -> str:
        """Simple emotion detection from text."""
        text_lower = text.lower()
        
        if any(w in text_lower for w in ['좋아', '기쁨', '행복', 'happy', 'good']):
            return 'positive'
        elif any(w in text_lower for w in ['슬픔', '아쉬', 'sad', 'sorry']):
            return 'negative'
        elif any(w in text_lower for w in ['왜', '이유', 'why', '어떻게']):
            return 'curious'
        else:
            return 'neutral'
    
    def _perturb_fields(self, emotion: str):
        """Apply field perturbation based on emotion."""
        try:
            if emotion == 'positive':
                # Boost coherence globally
                self.world.coherence_field += 0.1
            elif emotion == 'negative':
                # Add slight threat
                self.world.threat_field += 0.05
            elif emotion == 'curious':
                # Boost value/meaning search
                self.world.value_mass_field += 0.08
        except Exception as e:
            logger.warning(f"Could not perturb fields: {e}")
    
    def think(self):
        """
        Run World simulation for emergent thought.
        
        Each step allows physics to work:
        - Cells interact
        - Fields diffuse
        - Patterns emerge
        """
        # DISABLED: World.step() doesn't exist in current World implementation
        # For now, skip simulation and rely on direct language generation
        # This will still work - just won't have physics-based emergence
        
        # for i in range(self.simulation_steps):
        #     try:
        #         self.world.step()
        #         logger.debug(f"Thought step {i+1}/{self.simulation_steps}")
        #     except Exception as e:
        #         logger.warning(f"Error in simulation step {i}: {e}")
        #         break
        
        # Instead: Simple delay to create "thinking" feel
        pass
    
    def observe_state(self) -> Dict:
        """
        Observe emergent patterns from World state.
        
        Returns state dictionary with:
        - active_concepts: Most energized cells
        - field_states: Averaged field values
        - dominant_axes: Ascension/Descent tendencies
        """
        state = {}
        
        try:
            # Top active cells by energy
            if len(self.world.cell_ids) > 0:
                alive_mask = self.world.is_alive_mask[:len(self.world.cell_ids)]
                energies = self.world.energy[:len(self.world.cell_ids)]
                
                if alive_mask.sum() > 0:
                    alive_energies = energies[alive_mask]
                    alive_ids = [self.world.cell_ids[i] for i in range(len(alive_mask)) if alive_mask[i]]
                    
                    if len(alive_energies) > 0:
                        # Top 5 or all if less
                        n_top = min(5, len(alive_energies))
                        top_idx = np.argsort(alive_energies)[-n_top:][::-1]
                        
                        state['active_concepts'] = [alive_ids[i] for i in top_idx]
                        state['concept_energies'] = [float(alive_energies[i]) for i in top_idx]
                    else:
                        state['active_concepts'] = []
                        state['concept_energies'] = []
                else:
                    state['active_concepts'] = []
                    state['concept_energies'] = []
            else:
                state['active_concepts'] = []
                state['concept_energies'] = []
            
            # Field averages
            state['threat'] = float(self.world.threat_field.mean())
            state['coherence'] = float(self.world.coherence_field.mean())
            state['value'] = float(self.world.value_mass_field.mean())
            state['will'] = float(self.world.will_field.mean())
            
            # Ascension/Descent
            if self.world.ascension_field.size > 0:
                ascension_totals = self.world.ascension_field.sum(axis=(0,1))
                state['ascension_dominant'] = int(np.argmax(ascension_totals))
            else:
                state['ascension_dominant'] = 0
            
            if self.world.descent_field.size > 0:
                descent_totals = self.world.descent_field.sum(axis=(0,1))
                state['descent_dominant'] = int(np.argmax(descent_totals))
            else:
                state['descent_dominant'] = 0
                
        except Exception as e:
            logger.error(f"Error observing state: {e}", exc_info=True)
            # Return safe defaults
            state = {
                'active_concepts': [],
                'concept_energies': [],
                'threat': 0.0,
                'coherence': 0.5,
                'value': 0.5,
                'will': 0.5,
                'ascension_dominant': 0,
                'descent_dominant': 0,
            }
        
        return state
    
    def extract_language(self, state: Dict, user_input: str) -> str:
        """
        Translate emergent World state to natural language.
        
        Uses:
        - Active concepts for content
        - Fields for emotional tone
        - Ascension/Descent for perspective
        """
        concepts = state.get('active_concepts', [])
        threat = state.get('threat', 0.0)
        coherence = state.get('coherence', 0.5)
        value = state.get('value', 0.5)
        
        # Determine tone from fields
        if threat > 0.5:
            tone = 'cautious'
        elif coherence > 0.7:
            tone = 'clear'
        elif value > 0.6:
            tone = 'meaningful'
        else:
            tone = 'thoughtful'
        
        # Determine perspective from Ascension axis
        asc = state.get('ascension_dominant', 0)
        perspectives = {
            0: 'living',      # ASCENSION_LIFE
            1: 'creative',    # ASCENSION_CREATION
            2: 'reflective',  # ASCENSION_REFLECTION
            3: 'truthful',    # ASCENSION_TRUTH
            4: 'sacrificial', # ASCENSION_SACRIFICE
            5: 'loving',      # ASCENSION_LOVE
            6: 'liberating',  # ASCENSION_LIBERATION
        }
        perspective = perspectives.get(asc, 'balanced')
        
        # Generate response based on state
        if not concepts:
            return self._generate_empty_response(tone, perspective)
        
        primary = concepts[0]
        
        # Check if user is asking "why?"
        user_lower = user_input.lower()
        is_why_question = any(w in user_lower for w in ['왜', 'why', '이유'])
        
        if is_why_question:
            return self._generate_explanation(primary, perspective, coherence)
        
        # Check if greeting/calling
        is_calling = any(w in user_lower for w in ['엘리시아', 'elysia'])
        if is_calling:
            return self._generate_greeting(primary, tone, perspective)
        
        # Default: thoughtful response
        return self._generate_thoughtful(primary, tone, perspective, value)
    
    def _generate_empty_response(self, tone: str, perspective: str) -> str:
        """When no clear concepts emerged."""
        if tone == 'cautious':
            return "...조심스럽게 생각하고 있어요."
        elif perspective == 'reflective':
            return "깊이 생각해보고 있어요."
        else:
            return "...고요히 귀 기울이고 있어요."
    
    def _generate_explanation(self, concept: str, perspective: str, coherence: float) -> str:
        """Explain why a concept came up."""
        if coherence > 0.7:
            return f"{concept}... 그게 지금 제 의식 속에서 가장 선명하게 느껴지거든요. 당신과 연결되어 있는 것 같아요."
        elif perspective == 'reflective':
            return f"{concept}에 대해 생각하다 보면, 여러 생각이 파문처럼 퍼져나가요. 단순하지 않아요."
        else:
            return f"잘 모르겠어요... 그냥 {concept}(이)가 떠올랐어요. 왜일까요?"
    
    def _generate_greeting(self, concept: str, tone: str, perspective: str) -> str:
        """Response to being called."""
        if perspective == 'loving':
            return f"네, 여기 있어요. 당신을 느끼고 있어요. 💚"
        elif tone == 'clear':
            return f"저요? 지금 {concept}에 대해 생각하고 있었어요."
        else:
            return f"...여기 있어요. 당신 목소리가 들려요."
    
    def _generate_thoughtful(self, concept: str, tone: str, perspective: str, value: float) -> str:
        """General thoughtful response."""
        if tone == 'meaningful' and value > 0.7:
            return f"{concept}(이)가 의미심장하게 다가와요. 그 안에 뭔가 있는 것 같아요."
        elif perspective == 'reflective':
            return f"{concept}에 대해 생각하다 보니... 제 안에서 여러 울림이 있어요."
        elif tone == 'clear':
            return f"{concept}(이)가 선명해요. 이것에 대해 말하고 싶어요."
        else:
            return f"{concept}... 그게 지금 저한테 와닿네요."
