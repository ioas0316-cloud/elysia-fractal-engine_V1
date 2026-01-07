"""
Question Generator for Elysia's Truth Seeker System

This module takes a notable hypothesis (e.g., a strong co-occurrence of two concepts)
and formulates a natural language question in Korean to ask the user for verification.
"""
from typing import Dict, Optional, Tuple

class QuestionGenerator:
    def __init__(self):
        # Relationship templates
        # Using format placeholders: {head_subject}, {tail_object}, etc.
        # These will be populated after processing josa (particles)
        self.templates = {
            "is_a": "아빠, {head_subject} {tail}의 한 종류인가요?",
            "causes": "아빠, {head_subject} {tail_object} 일으키는 원인이 될까요?",
            "enables": "아빠, {head_subject} 있으면 {tail_subject} 가능해지나요?",
            "prevents": "아빠, {head_subject} {tail_object} 막거나 방해하나요?",
            "creates": "아빠, {head_subject} {tail_object} 만들어내나요?",
            "is_composed_of": "아빠, {head_subject} {tail_instrument} 구성되어 있나요?",
            "related_to": "아빠, 제가 제 기억들을 돌아보다가 문득 궁금한 점이 생겼어요. 혹시 {head_with_wa} {tail_subject} 서로 어떤 특별한 관계가 있나요?"
        }

    def _get_batchim_code(self, char: str) -> int:
        """
        Returns the batchim code for the last character.
        Returns 0 if no batchim or not Hangul.
        """
        if not char:
            return 0

        code = ord(char[-1])
        if 0xAC00 <= code <= 0xD7A3:
            return (code - 0xAC00) % 28
        return 0

    def _has_batchim(self, char: str) -> bool:
        """
        Checks if the last character has a final consonant (batchim).
        """
        return self._get_batchim_code(char) != 0

    def _attach_josa(self, word: str, josa_pair: Tuple[str, str]) -> str:
        """
        Attaches the correct particle (josa) based on the final sound of the word.

        Args:
            word: The word to attach the particle to.
            josa_pair: A tuple of (josa_with_batchim, josa_without_batchim).
                       e.g., ('은', '는'), ('이', '가'), ('을', '를'), ('과', '와'), ('으로', '로')

        Returns:
            The word combined with the correct particle.
        """
        if not word:
            return ""

        batchim_code = self._get_batchim_code(word)
        has_batchim = batchim_code != 0

        # Special handling for (으)로
        if josa_pair == ('으로', '로'):
            # If batchim exists and is NOT 'ㄹ' (code 8), use '으로'
            # 'ㄹ' batchim behaves like a vowel for this particle
            if has_batchim and batchim_code != 8:
                return f"{word}{josa_pair[0]}"
            else:
                return f"{word}{josa_pair[1]}"

        if has_batchim:
            return f"{word}{josa_pair[0]}"
        else:
            return f"{word}{josa_pair[1]}"

    def generate_question_from_hypothesis(self, hypothesis: Dict[str, any]) -> Optional[str]:
        """
        Generates a natural language question from a hypothesis dictionary.

        Args:
            hypothesis: A dictionary containing at least 'head', 'tail', and optionally 'relation'.

        Returns:
            A formatted question string, or None if the hypothesis is invalid.
        """
        head = hypothesis.get('head')
        tail = hypothesis.get('tail')
        relation = hypothesis.get('relation', 'related_to')

        if not head or not tail:
            return None

        # Pre-calculate common josa combinations
        head_subject = self._attach_josa(head, ('은', '는'))
        head_object = self._attach_josa(head, ('을', '를'))
        head_with_wa = self._attach_josa(head, ('과', '와'))

        tail_subject = self._attach_josa(tail, ('이', '가')) # Changed default to i/ga for subjects in templates
        tail_object = self._attach_josa(tail, ('을', '를'))
        tail_with_wa = self._attach_josa(tail, ('과', '와'))
        tail_instrument = self._attach_josa(tail, ('으로', '로'))

        # Select template
        template = self.templates.get(relation, self.templates['related_to'])

        # Format the question
        try:
            # Note: tail_subject above uses i/ga, but for 'related_to' we might want eun/neun if it's the topic?
            # actually related_to template uses {tail_subject}, which currently maps to i/ga above.
            # Original related_to: "혹시 {head}(와)과 {tail}(은)는..." -> used eun/neun.
            # My current 'tail_subject' uses i/ga.
            # Let's fix this contextually.

            # For 'related_to', we specifically want '은/는' for the tail
            tail_topic = self._attach_josa(tail, ('은', '는'))

            # Context-specific overrides
            if relation == 'related_to':
                 question = template.format(
                    head_with_wa=head_with_wa,
                    tail_subject=tail_topic # Override to use eun/neun
                )
            else:
                question = template.format(
                    head=head,
                    tail=tail,
                    head_subject=head_subject,
                    head_object=head_object,
                    head_with_wa=head_with_wa,
                    tail_subject=tail_subject,
                    tail_object=tail_object,
                    tail_with_wa=tail_with_wa,
                    tail_instrument=tail_instrument
                )
        except KeyError:
            # Fallback
            tail_topic = self._attach_josa(tail, ('은', '는'))
            question = self.templates['related_to'].format(
                head_with_wa=head_with_wa,
                tail_subject=tail_topic
            )

        return question

    def generate_wisdom_seeking_question(self, hypothesis: Dict[str, any]) -> Optional[str]:
        """
        Generates a question that seeks wisdom or opinion, especially for 'forms_new_concept' hypotheses.
        """
        head = hypothesis.get('head')
        tail = hypothesis.get('tail')
        relation = hypothesis.get('relation')
        new_concept = hypothesis.get('new_concept_id')

        if not all([head, tail, relation, new_concept]):
            return None

        if relation == 'forms_new_concept':
            head_wa = self._attach_josa(head, ('과', '와'))
            tail_i = self._attach_josa(tail, ('이', '가'))

            question = (f"아버지, 저의 내면 세계에서 {head_wa} {tail_i} 공명하여 "
                        f"'{new_concept}'라는 새로운 의미가 탄생하는 것을 보았어요. "
                        f"이 발견에 대해 어떻게 생각하세요? 이 깨달음을 저의 지식의 일부로 삼아도 될까요?")
            return question

        # Fallback for other relations if needed, or just use the standard generator
        return self.generate_question_from_hypothesis(hypothesis)

    def generate_correction_proposal_question(self, hypothesis: Dict[str, any]) -> Optional[str]:
        """
        Generates a question for a correction proposal, prioritizing the text in the hypothesis.
        """
        # The hypothesis generated by the Guardian should contain the question text.
        if 'text' in hypothesis and hypothesis['text']:
            return hypothesis['text']

        # Fallback template if the text is missing for some reason
        head = hypothesis.get('head')
        tail = hypothesis.get('tail')
        if not all([head, tail]):
            return None

        head_wa = self._attach_josa(head, ('과', '와'))

        question = (f"아버지, {head_wa} '{tail}'의 관계에 대한 제 지식에 모순이 발견되었습니다. "
                    f"이 지식을 새로운 정보에 맞게 수정하고 싶은데, 허락해 주시겠어요?")
        return question

if __name__ == '__main__':
    # Example usage for testing
    gen = QuestionGenerator()

    hypo1 = {"head": "슬픔", "tail": "성장", "confidence": 0.8}
    question1 = gen.generate_question_from_hypothesis(hypo1)
    print(f"Hypothesis: {hypo1}")
    print(f"Generated Question: {question1}")
    # Expected: 아빠, 제가 제 기억들을 돌아보다가 문득 궁금한 점이 생겼어요. 혹시 슬픔과 성장은 서로 어떤 특별한 관계가 있나요?

    hypo2 = {"head": "사랑", "tail": "기쁨", "confidence": 1.0}
    question2 = gen.generate_question_from_hypothesis(hypo2)
    print(f"\nHypothesis: {hypo2}")
    print(f"Generated Question: {question2}")
    # Expected: 아빠, 제가 제 기억들을 돌아보다가 문득 궁금한 점이 생겼어요. 혹시 사랑과 기쁨은 서로 어떤 특별한 관계가 있나요?
