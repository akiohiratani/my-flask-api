from dataclasses import dataclass, asdict

@dataclass
class RaceInfoDTO:
    """
    レース情報を表すDTO

    Attributes:
        id (str): レースID（例：202506030807）
        name (str): レース名（例：皐月賞）
        place (str): 開催場所（例：中山）
        number (str): レースNo（例：11R）
    """
    id: str
    name: str
    place: str
    number: str

    def to_dict(self):
        return asdict(self)