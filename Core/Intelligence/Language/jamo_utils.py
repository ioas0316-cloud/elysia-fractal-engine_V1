"""
Jamo Utility Module
===================

Provides functions to decompose Hangul syllables into Jamo (Initial, Medial, Final).
Standard Unicode algorithm:
  Index = ((Initial * 21) + Medial) * 28 + Final + 0xAC00

[NEW 2025-12-16] Created for Phonetic Resonance Layer
"""

# Unicode Constants
BASE_CODE = 0xAC00  # '가'
LIMIT_CODE = 0xD7A3  # '힣' (Last Hangul Syllable)

# Lists of Jamos
CHOSUNG_LIST = [
    'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ',
    'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
]

JUNGSUNG_LIST = [
    'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ',
    'ㅙ', 'ㅚ', '(표현불가)', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ'
]
# Note: In standard sequence, index 12 is 'ㅛ' but I put marker. Let's fix.
# Correct Order:
# ㅏ ㅐ ㅑ ㅒ ㅓ ㅔ ㅕ ㅖ ㅗ ㅘ ㅙ ㅚ ㅛ ㅜ ㅝ ㅞ ㅟ ㅠ ㅡ ㅢ ㅣ
JUNGSUNG_LIST = [
    'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ',
    'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ'
]

JONGSUNG_LIST = [
    ' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ',
    'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ',
    'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
]
# ' ' is empty final consonant

def is_hangul(char: str) -> bool:
    """Checks if a character is a Hangul syllable."""
    if not char: return False
    code = ord(char)
    return BASE_CODE <= code <= LIMIT_CODE

def decompose_hangul(char: str) -> tuple:
    """
    Decomposes a Hangul syllable into (Initial, Medial, Final).
    Returns (None, None, None) if not Hangul.
    """
    if not is_hangul(char):
        return None, None, None

    code = ord(char) - BASE_CODE

    jong = code % 28
    code //= 28
    jung = code % 21
    cho = code // 21

    return CHOSUNG_LIST[cho], JUNGSUNG_LIST[jung], JONGSUNG_LIST[jong]

def get_jamo_string(char: str) -> str:
    """Returns Jamos joined as a string (e.g., '가' -> 'ㄱㅏ ')."""
    c, j, k = decompose_hangul(char)
    if not c:
        return char
    return f"{c}{j}{k if k != ' ' else ''}"
