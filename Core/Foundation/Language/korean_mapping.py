# -*- coding: utf-8 -*-
"""
한영 개념 매핑
==============

영어 개념 → 한국어 이름 매핑
"""

# 기본 한영 사전
KOREAN_MAPPING = {
    # 감정
    'Love': '사랑',
    'Joy': '기쁨',
    'Sadness': '슬픔',
    'Fear': '두려움',
    'Anger': '분노',
    'Trust': '신뢰',
    'Hope': '희망',
    'Happiness': '행복',
    
    # 행동
    'Learning': '배움',
    'Teaching': '가르침',
    'Creating': '창조',
    'Thinking': '생각',
    'Communication': '소통',
    'Movement': '움직임',
    'Building': '건설',
    
    # 개념
    'Freedom': '자유',
    'Justice': '정의',
    'Truth': '진실',
    'Beauty': '아름다움',
    'Wisdom': '지혜',
    'Knowledge': '지식',
    'Time': '시간',
    
    # 관계
    'Friendship': '우정',
    'Family': '가족',
    'Community': '공동체',
    'Society': '사회',
    
    # 자연
    'Light': '빛',
    'Water': '물',
    'Fire': '불',
    'Earth': '땅',
    'Air': '공기',
    'Ocean': '바다',
    'Forest': '숲',
    'Mountain': '산',
    'River': '강',
    'Desert': '사막',
    'Climate': '기후',
    'Season': '계절',
    
    # 과학
    'Physics': '물리학',
    'Chemistry': '화학',
    'Biology': '생물학',
    'Astronomy': '천문학',
    'Geology': '지질학',
    'Mathematics': '수학',
    'Ecology': '생태학',
    'Genetics': '유전학',
    
    # 기술
    'Computer': '컴퓨터',
    'Internet': '인터넷',
    'Software': '소프트웨어',
    'Algorithm': '알고리즘',
    'Data': '데이터',
    'Programming': '프로그래밍',
    
    # 예술
    'Music': '음악',
    'Painting': '그림',
    'Sculpture': '조각',
    'Dance': '춤',
    'Poetry': '시',
    'Theater': '연극',
    'Architecture': '건축',
    
    # 사회
    'Politics': '정치',
    'Economics': '경제',
    'Law': '법',
    'Education': '교육',
    'Culture': '문화',
    'Religion': '종교',
    'Ethics': '윤리',
    
    # 인간
    'Consciousness': '의식',
    'Memory': '기억',
    'Perception': '지각',
    'Reasoning': '추론',
    'Creativity': '창의성',
    'Will': '의지',
    'Identity': '정체성',
    
    # 관계 행동
    'Cooperation': '협력',
    'Competition': '경쟁',
    'Conflict': '갈등',
    'Collaboration': '협업',
    'Leadership': '리더십',
    'Empathy': '공감',
    
    # 추상
    'Infinity': '무한',
    'Eternity': '영원',
    'Nothing': '무',
    'Everything': '만물',
    'Possible': '가능',
    'Necessary': '필연',
    'Contingent': '우연',
}

def get_korean_name(english_name: str) -> str:
    """영어 개념명 → 한국어"""
    return KOREAN_MAPPING.get(english_name, "")

def add_mapping(english: str, korean: str):
    """새 매핑 추가 (학습 중 확장)"""
    KOREAN_MAPPING[english] = korean
