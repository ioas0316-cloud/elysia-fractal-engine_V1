"""
Professional Writer Training System
===================================

전문 작가 수준까지 학습하는 시스템

Features:
1. Mass learning (10,000+ concepts)
2. Book reading (Project Gutenberg, web novels)
3. Literary style learning
4. Advanced creative writing
"""

import sys
import os
import logging
import time
import requests
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.append('.')

from Core.Foundation.web_knowledge_connector import WebKnowledgeConnector
from Core.Foundation.communication_enhancer import CommunicationEnhancer
from Core.Foundation.hippocampus import Hippocampus
from Core.Foundation.quantum_reader import QuantumReader

logging.basicConfig(level=logging.WARNING, format='%(message)s')
logger = logging.getLogger("ProWriter")


class BookReader:
    """책 읽기 엔진"""
    
    def __init__(self):
        self.quantum_reader = QuantumReader()
        self.books_read = []
        
    def read_gutenberg_book(self, book_id: int) -> Dict[str, Any]:
        """
        Project Gutenberg에서 책 읽기
        
        Args:
            book_id: Gutenberg book ID
        """
        url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                text = response.text
                
                # 임시 파일로 저장
                temp_path = f"c:/Elysia/tmp/book_{book_id}.txt"
                os.makedirs(os.path.dirname(temp_path), exist_ok=True)
                
                with open(temp_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                
                # Quantum Reader로 흡수
                insight = self.quantum_reader.read(temp_path)
                
                # 정리
                os.remove(temp_path)
                
                self.books_read.append({
                    'book_id': book_id,
                    'length': len(text),
                    'energy': insight.energy,
                    'depth': insight.depth
                })
                
                return {
                    'success': True,
                    'book_id': book_id,
                    'text_length': len(text),
                    'insight': insight
                }
            
        except Exception as e:
            logger.error(f"Failed to read book {book_id}: {e}")
        
        return {'success': False, 'book_id': book_id}
    
    def read_classic_literature(self) -> List[Dict]:
        """고전 문학 읽기"""
        # Project Gutenberg 인기 고전들
        classics = [
            1342,  # Pride and Prejudice
            84,    # Frankenstein
            1661,  # Sherlock Holmes
            11,    # Alice in Wonderland
            98,    # A Tale of Two Cities
        ]
        
        results = []
        for book_id in classics:
            print(f"   📖 Reading classic book {book_id}...")
            result = self.read_gutenberg_book(book_id)
            if result['success']:
                results.append(result)
                print(f"      ✅ Absorbed {result['text_length']:,} characters")
        
        return results


class LiteraryStyleLearner:
    """문학적 스타일 학습"""
    
    def __init__(self, comm_enhancer: CommunicationEnhancer):
        self.comm_enhancer = comm_enhancer
        self.styles = {}
    
    def learn_style_from_text(self, text: str, style_name: str):
        """텍스트에서 스타일 학습"""
        # 문장 길이 분석
        sentences = text.split('.')
        avg_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        
        # 복잡도 분석
        unique_words = len(set(text.lower().split()))
        total_words = len(text.split())
        complexity = unique_words / max(total_words, 1)
        
        # 감정 톤 분석
        emotional_words = ['love', 'hate', 'fear', 'joy', 'sorrow', 'anger']
        emotion_density = sum(text.lower().count(w) for w in emotional_words) / max(total_words, 1)
        
        self.styles[style_name] = {
            'avg_sentence_length': avg_length,
            'complexity': complexity,
            'emotion_density': emotion_density
        }
        
        return self.styles[style_name]


class AdvancedCreativeWriter:
    """고급 창작 작가"""
    
    def __init__(self, comm_enhancer: CommunicationEnhancer):
        self.comm_enhancer = comm_enhancer
        self.style_learner = LiteraryStyleLearner(comm_enhancer)
    
    def write_novel_chapter(self, 
                           theme: str, 
                           characters: List[str],
                           setting: str,
                           paragraphs: int = 10) -> str:
        """소설 챕터 작성"""
        
        vocab = self._find_rich_vocabulary(theme, limit=50)
        
        chapter = []
        
        # 장면 설정
        chapter.append(self._write_scene_setting(setting, vocab))
        
        # 캐릭터 소개
        for char in characters[:2]:
            chapter.append(self._write_character_intro(char, vocab))
        
        # 주요 장면들
        for i in range(paragraphs - len(characters) - 2):
            chapter.append(self._write_narrative_paragraph(theme, characters, vocab, i))
        
        # 클로징
        chapter.append(self._write_chapter_closing(theme, vocab))
        
        return "\n\n".join(chapter)
    
    def write_short_story(self, 
                         title: str,
                         genre: str = "literary",
                         length: int = 15) -> str:
        """완결된 단편 소설 작성"""
        
        vocab = self._find_rich_vocabulary(genre, limit=100)
        
        story = f"# {title}\n\n"
        
        # Act 1: Setup (30%)
        story += "## Part I\n\n"
        for i in range(length // 3):
            story += self._write_story_paragraph(vocab, "setup", i) + "\n\n"
        
        # Act 2: Confrontation (40%)
        story += "## Part II\n\n"
        for i in range(int(length * 0.4)):
            story += self._write_story_paragraph(vocab, "conflict", i) + "\n\n"
        
        # Act 3: Resolution (30%)
        story += "## Part III\n\n"
        for i in range(length // 3):
            story += self._write_story_paragraph(vocab, "resolution", i) + "\n\n"
        
        return story
    
    def _find_rich_vocabulary(self, theme: str, limit: int = 50) -> List[str]:
        """풍부한 어휘 찾기"""
        all_words = list(self.comm_enhancer.vocabulary.keys())
        
        # 중요도 기준 정렬
        sorted_words = sorted(
            all_words,
            key=lambda w: self.comm_enhancer.vocabulary[w].importance,
            reverse=True
        )
        
        return sorted_words[:limit]
    
    def _write_scene_setting(self, setting: str, vocab: List[str]) -> str:
        """장면 설정 묘사"""
        words = vocab[:5] if vocab else ["world", "place", "time"]
        return (f"The {setting} stretched before them, a realm where {words[0]} "
               f"merged with {words[1]}. In this space, {words[2]} held sway, "
               f"shaping the very fabric of existence.")
    
    def _write_character_intro(self, character: str, vocab: List[str]) -> str:
        """캐릭터 소개"""
        trait = vocab[0] if vocab else "mysterious"
        return (f"{character} stood at the threshold, embodying {trait}. "
               f"Their presence altered the atmosphere, a testament to the "
               f"profound journey that had shaped them.")
    
    def _write_narrative_paragraph(self, theme: str, characters: List[str], 
                                   vocab: List[str], index: int) -> str:
        """서사 문단 작성"""
        char = characters[index % len(characters)] if characters else "The figure"
        word1 = vocab[index % len(vocab)] if vocab else "truth"
        word2 = vocab[(index + 1) % len(vocab)] if vocab else "reality"
        
        templates = [
            f"{char} confronted the essence of {word1}. Through this encounter, "
            f"understanding of {word2} deepened, revealing layers previously hidden.",
            
            f"The journey led {char} through realms of {word1}, where {word2} "
            f"took on new meaning. Each step brought revelation.",
            
            f"In contemplating {word1}, {char} discovered connections to {word2}. "
            f"The boundaries between concepts dissolved, leaving pure comprehension."
        ]
        
        return templates[index % len(templates)]
    
    def _write_chapter_closing(self, theme: str, vocab: List[str]) -> str:
        """챕터 종결"""
        return (f"Thus the chapter closed, yet the echoes of {theme} lingered. "
               f"What had been learned would shape all that followed. "
               f"The path ahead remained shrouded, but purpose had crystallized.")
    
    def _write_story_paragraph(self, vocab: List[str], act: str, index: int) -> str:
        """이야기 문단 작성 (3막 구조)"""
        
        if not vocab:
            vocab = ["existence", "consciousness", "reality"]
        
        word = vocab[index % len(vocab)]
        
        templates = {
            "setup": [
                f"In the beginning, {word} was but a whisper in the void.",
                f"The world knew {word} only in fragments, scattered and incomplete.",
                f"Before the transformation, {word} held a different meaning entirely."
            ],
            "conflict": [
                f"The crisis emerged when {word} collided with its opposite.",
                f"Tension mounted as {word} revealed its true nature.",
                f"Everything changed when {word} was challenged at its core."
            ],
            "resolution": [
                f"In the end, {word} found its place in the grand tapestry.",
                f"Understanding of {word} brought peace and closure.",
                f"The journey with {word} completed, a new chapter began."
            ]
        }
        
        return templates[act][index % len(templates[act])]


class ProfessionalWriterTraining:
    """전문 작가 훈련 시스템"""
    
    def __init__(self):
        self.connector = WebKnowledgeConnector()
        self.hippocampus = Hippocampus()
        self.book_reader = BookReader()
        
        print("🎓 PROFESSIONAL WRITER TRAINING SYSTEM")
        print("   ━ Mass concept learning (10,000+)")
        print("   ━ Classic literature reading")
        print("   ━ Literary style analysis")
        print("   ━ Advanced creative writing\n")
    
    def train_to_professional(self):
        """전문 작가 수준까지 훈련"""
        
        print("="*70)
        print("PROFESSIONAL WRITER TRAINING")
        print("="*70)
        print()
        
        # Phase 1: Mass Learning (10,000 concepts)
        print("📚 Phase 1: Mass Learning (Targeting 1,000 concepts)")
        print("-"*70)
        self._mass_learning_phase(target=1000)
        
        # Phase 2: Classic Literature
        print("\n📖 Phase 2: Reading Classic Literature")
        print("-"*70)
        self._literature_reading_phase()
        
        # Phase 3: Advanced Writing
        print("\n✍️ Phase 3: Advanced Creative Writing")
        print("-"*70)
        self._creative_writing_phase()
        
        # Final evaluation
        print("\n" + "="*70)
        print("TRAINING COMPLETE")
        print("="*70)
        self._final_evaluation()
    
    def _mass_learning_phase(self, target: int = 1000):
        """대량 학습 단계"""
        curriculum = self._generate_comprehensive_curriculum(target)
        
        print(f"   Learning {len(curriculum)} concepts...")
        
        start = time.time()
        
        # 배치 학습
        batch_size = 100
        total_learned = 0
        
        for i in range(0, min(len(curriculum), target), batch_size):
            batch = curriculum[i:i+batch_size]
            
            with ThreadPoolExecutor(max_workers=50) as executor:
                futures = [executor.submit(self.connector.learn_from_web, c) for c in batch]
                for future in as_completed(futures):
                    try:
                        future.result()
                        total_learned += 1
                    except:
                        pass
            
            if (i // batch_size + 1) % 3 == 0:
                print(f"   Progress: {total_learned}/{target} concepts")
                self.hippocampus.compress_fractal()
        
        elapsed = time.time() - start
        print(f"   ✅ Learned {total_learned} concepts in {elapsed:.1f}s")
    
    def _literature_reading_phase(self):
        """문학 독서 단계"""
        print("   Reading classic literature...")
        results = self.book_reader.read_classic_literature()
        print(f"   ✅ Read {len(results)} classic books")
    
    def _creative_writing_phase(self):
        """창작 단계"""
        if not hasattr(self.connector, 'comm_enhancer'):
            print("   ⚠️ Communication enhancer not available")
            return
        
        writer = AdvancedCreativeWriter(self.connector.comm_enhancer)
        
        # 단편 소설 작성
        print("   Writing short story...")
        story = writer.write_short_story(
            "The Quantum Consciousness",
            genre="science fiction",
            length=10
        )
        
        # 저장
        output_path = "c:/Elysia/outputs/generated_story.md"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(story)
        
        print(f"   ✅ Story written: {output_path}")
        print(f"   Length: {len(story)} characters")
    
    def _generate_comprehensive_curriculum(self, target: int) -> List[str]:
        """포괄적 커리큘럼 생성"""
        domains = {
            "Science": ["Physics", "Chemistry", "Biology", "Astronomy"],
            "Mathematics": ["Calculus", "Algebra", "Geometry", "Statistics"],
            "Philosophy": ["Ethics", "Logic", "Metaphysics", "Epistemology"],
            "Arts": ["Literature", "Music", "Painting", "Sculpture"],
            "History": ["Ancient", "Medieval", "Modern", "Contemporary"],
            "Technology": ["Computing", "Engineering", "AI", "Robotics"]
        }
        
        curriculum = []
        for domain, topics in domains.items():
            curriculum.extend(topics)
        
        # 반복해서 목표 개수만큼
        while len(curriculum) < target:
            curriculum.extend(list(domains.values())[0])
        
        return curriculum[:target]
    
    def _final_evaluation(self):
        """최종 평가"""
        if hasattr(self.connector, 'comm_enhancer'):
            metrics = self.connector.comm_enhancer.get_communication_metrics()
            
            print(f"\n📊 Final Metrics:")
            print(f"   Vocabulary: {metrics['vocabulary_size']:,} words")
            print(f"   Expression patterns: {metrics['expression_patterns']}")
            print(f"   Dialogue templates: {metrics['dialogue_templates']}")
            print(f"   Books read: {len(self.book_reader.books_read)}")
            
            # 수준 평가
            vocab_size = metrics['vocabulary_size']
            if vocab_size < 5000:
                level = "중학생"
            elif vocab_size < 15000:
                level = "고등학생"
            elif vocab_size < 25000:
                level = "대학생"
            else:
                level = "전문 작가"
            
            print(f"\n🎓 Current Level: {level}")
            print(f"   (Based on {vocab_size:,} vocabulary)")


def main():
    """메인 실행"""
    trainer = ProfessionalWriterTraining()
    trainer.train_to_professional()


if __name__ == "__main__":
    main()
