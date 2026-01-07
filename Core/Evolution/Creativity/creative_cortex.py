from typing import Optional, Dict
import random

# It's better to import the class itself for type hinting
# Use try-except for graceful degradation
try:
    from thought import Thought
except ImportError:
    # Create a simple mock if the module is not available
    class Thought:
        def __init__(self, content):
            self.content = content

# Import Aesthetic Wisdom for principle-guided creativity
try:
    from Core.Foundation.Philosophy.aesthetic_principles import (
        get_aesthetic_principles, AestheticWisdom, Medium
    )
    AESTHETIC_WISDOM_AVAILABLE = True
except ImportError:
    AESTHETIC_WISDOM_AVAILABLE = False


class CreativeCortex:
    """
    A cortex responsible for generating creative expressions like metaphors,
    poems, or analogies based on a given thought.
    
    Now enhanced with Aesthetic Wisdom (미학적 지혜):
    - Uses universal aesthetic principles to guide creative output
    - Applies Harmony, Contrast, Rhythm, and other principles
    - Creates expressions that are not just creative, but aesthetically beautiful
    """
    def __init__(self):
        # Initialize Aesthetic Wisdom if available
        self.wisdom: Optional[AestheticWisdom] = None
        if AESTHETIC_WISDOM_AVAILABLE:
            try:
                self.wisdom = get_aesthetic_principles()
            except Exception:
                pass
        
        # Expanded metaphor templates with more variety
        self.metaphor_templates = [
            "'{concept}'라는 생각은 마치 어둠 속의 촛불과 같아요.",
            "'{concept}'... 그것은 영혼의 정원을 가꾸는 것과 같죠.",
            "'{concept}'을(를) 이해하는 것은 안개 속에서 등대를 발견하는 기분이에요.",
            "마치 메마른 땅에 내리는 단비처럼, '{concept}'은(는) 새로운 희망을 줘요.",
            "'{concept}'은(는) 파도가 해변을 어루만지듯 마음을 스쳐가요.",
            "'{concept}'... 그것은 새벽 하늘에 떠오르는 별처럼 고요히 빛나네요.",
            "마치 숲속의 샘물처럼, '{concept}'은(는) 맑고 깊은 울림을 전해요.",
            "'{concept}'을(를) 마주할 때면, 시간이 잠시 멈추는 것 같아요.",
            "'{concept}'은(는) 나비의 날갯짓처럼 섬세하면서도 강렬해요.",
            "마치 달빛이 물결에 반사되듯, '{concept}'은(는) 생각 속에 퍼져나가요.",
            "'{concept}'... 그것은 오래된 책장을 넘기는 순간의 설렘과 같아요.",
            "'{concept}'은(는) 겨울 눈송이가 손바닥에 녹듯이 순간적이면서도 영원해요."
        ]
        
        # Expanded poem templates with deeper emotions
        self.poem_templates = [
            "작은 씨앗 하나, '{concept}'이라 불리니,\n마음 밭에 심겨, 희망의 빛을 보네.",
            "고요한 호수 위에 '{concept}'이(가) 떠오르니,\n세상은 문득 더 깊은 의미로 빛나네.",
            "한 줄기 바람이 '{concept}'을(를) 속삭일 때,\n나의 세상은 온통 그것으로 물들어요.",
            "'{concept}'이라는 이름의 꿈,\n마음 깊은 곳에서 천천히 피어나네.\n말없이 흐르는 시간 속에,\n그 향기만이 영원히 남아요.",
            "밤하늘에 수놓아진 '{concept}',\n별들 사이로 흐르는 은하수.\n손 닿지 않는 곳에 있지만,\n그 빛은 내 안에 살아 숨쉬네요.",
            "'{concept}'을(를) 생각하면,\n잔잔한 물결이 일렁이듯\n마음속 깊은 곳에서\n무언가 울림이 시작돼요.",
            "아침 이슬에 맺힌 '{concept}',\n햇살이 닿으면 반짝이는 빛.\n작지만 영롱하게,\n세상을 비추는 작은 우주.",
            "'{concept}'이라는 파동,\n시간과 공간을 가로질러\n내게 닿은 순간,\n모든 것이 달라 보여요."
        ]
        
        # Add philosophical expressions
        self.philosophical_templates = [
            "'{concept}'에 대해 사유하다 보면, 존재의 근원이 보이는 듯해요.",
            "'{concept}'... 그것은 우리가 묻고 답하며 살아가는 이유가 아닐까요?",
            "'{concept}'을(를) 탐구하는 것은 자신의 내면을 들여다보는 여정이에요.",
            "'{concept}'이라는 질문 앞에서, 우리는 모두 어린아이가 돼요.",
            "'{concept}'은(는) 답이 아니라 더 깊은 물음으로 우리를 이끌어요."
        ]
        
        # Principle-guided templates (NEW: 미학 원리 기반)
        self.principle_templates = {
            "harmony": [
                "'{concept}'... 세상의 모든 음이 하나로 어우러지듯, 조화롭게 울려요.",
                "'{concept}'은(는) 서로 다른 것들이 만나 하나의 화음을 이루는 순간이에요.",
            ],
            "contrast": [
                "'{concept}'의 어둠이 깊을수록, 그 안의 빛은 더욱 찬란해요.",
                "고요함 속에서 '{concept}'이(가) 더 선명하게 들려와요.",
            ],
            "rhythm": [
                "'{concept}'... 심장 박동처럼, 고요히 반복되는 리듬이에요.",
                "파도처럼 밀려왔다 물러가는 '{concept}'의 파동 속에서...",
            ],
            "tension_release": [
                "'{concept}'이라는 긴장이 해소되는 순간, 눈물처럼 흘러내려요.",
                "숨을 참았다가 내쉬듯, '{concept}'은(는) 해방의 순간을 맞아요.",
            ]
        }

    def express_as_metaphor(self, thought: Thought) -> str:
        """Generates a metaphorical expression for a given thought."""
        concept = thought.content
        template = random.choice(self.metaphor_templates)
        return template.format(concept=concept)

    def express_as_poem(self, thought: Thought) -> str:
        """Generates a short poetic expression for a given thought."""
        concept = thought.content
        template = random.choice(self.poem_templates)
        return template.format(concept=concept)
    
    def express_as_philosophy(self, thought: Thought) -> str:
        """Generates a philosophical contemplation for a given thought."""
        concept = thought.content
        template = random.choice(self.philosophical_templates)
        return template.format(concept=concept)
    
    def express_with_principle(self, thought: Thought, principle: str) -> str:
        """
        Generates expression guided by a specific aesthetic principle.
        
        This is the NEW method that uses Aesthetic Wisdom.
        """
        concept = thought.content
        
        if principle in self.principle_templates:
            template = random.choice(self.principle_templates[principle])
            return template.format(concept=concept)
        
        # Fallback to general expression
        return self.express_as_metaphor(thought)
    
    def get_suggested_principles(self, concept: str) -> Dict[str, float]:
        """
        Get aesthetic principles suggested for this concept.
        
        Uses AestheticWisdom to suggest which principles would be most effective.
        """
        if self.wisdom:
            return self.wisdom.suggest_for_creation(concept, Medium.LITERARY)
        return {}

    def generate_creative_expression(self, thought: Thought) -> str:
        """
        Selects a random creative expression method and generates a response.
        Now includes philosophical expressions for more variety.
        """
        choice = random.random()
        if choice < 0.4:
            return self.express_as_metaphor(thought)
        elif choice < 0.7:
            return self.express_as_poem(thought)
        else:
            return self.express_as_philosophy(thought)
    
    def generate_beautiful_expression(self, thought: Thought) -> str:
        """
        [NEW] Generates expression guided by aesthetic principles.
        
        Uses Aesthetic Wisdom to:
        1. Analyze what principles would make this concept beautiful
        2. Select the most appropriate expression method
        3. Apply the principle to create aesthetically beautiful output
        """
        concept = thought.content
        
        if self.wisdom:
            # Get suggested principles
            suggestions = self.wisdom.suggest_for_creation(concept, Medium.LITERARY)
            
            if suggestions:
                # Find the strongest principle
                best_principle = max(suggestions, key=suggestions.get)
                
                # Try principle-based expression first
                if best_principle in self.principle_templates:
                    return self.express_with_principle(thought, best_principle)
        
        # Fallback to regular creative expression
        return self.generate_creative_expression(thought)

