
from dataclasses import dataclass
from enum import Enum

@dataclass
class CosmicIncarnation:
    name: str
    color: str
    concept: str
    title: str
    function: str

class Ascension(Enum):
    VITARIAEL = CosmicIncarnation("Vitariael", "새벽 금빛", "Life", "상승의 시작", "생명 생성, 발아, 의식 탄생")
    EMETRIEL = CosmicIncarnation("Emetriel", "황금", "Creation", "구조를 만드는 힘", "존재가 형태를 갖추게 한다, 개념·언어·문명을 만든다")
    SOPHIEL = CosmicIncarnation("Sophiel", "은색 푸른빛", "Reflection", "위로 향하는 의식", "스스로를 비추고, 배움과 통찰을 얻음")
    GAVRIEL = CosmicIncarnation("Gavriel", "청명", "Truth", "왜곡되지 않은 수직성", "위아래가 명확해짐")
    SARAKHIEL = CosmicIncarnation("Sarakhiel", "붉은광", "Sacrifice", "자기 소모를 통한 상승", "나를 버려 전체를 높이는 힘")
    RAHAMIEL = CosmicIncarnation("Rafamiel", "분홍빛 백광", "Love", "중력의 반대, 확산", "모든 존재를 밖으로 확장시키며 들어올림")
    LUMIEL = CosmicIncarnation("Lumiel", "자외광", "Liberation", "상승의 끝, 해탈", "의식이 중심을 탈출하여 “위로” 나아가는 힘")

class Descent(Enum):
    MOTUS = CosmicIncarnation("Motus", "검은 자주", "Death", "하강의 기점", "생명의 파동이 0으로 수렴")
    SOLVARIS = CosmicIncarnation("Solvaris", "잿빛 검은색", "Dissolution", "형태 붕괴, 구조 분해", "구조 분해")
    OBSCURE = CosmicIncarnation("Obscure", "암청", "Ignorance", "반대방향으로 흐르는 의식", "상승이 아닌 정체와 회피")
    DIABOLOS = CosmicIncarnation("Diabolos", "검푸른 보라", "Distortion", "진실이 휘어지고 관점이 무너지는 단계", "왜곡")
    LUCIFEL = CosmicIncarnation("Lucifel", "불타는 검황", "Self-Obsession", "중심이 과하게 무거워져 붕괴", "이기")
    MAMMON = CosmicIncarnation("Mammon", "순흑", "Consumption", "외부를 끝없이 빨아들이는 블랙홀 단계", "탐욕")
    ASMODEUS = CosmicIncarnation("Asmodeus", "어둠 중의 어둠", "Bondage", "하강의 끝, 완전한 정지·감금", "속박")
