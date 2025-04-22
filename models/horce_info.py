from dataclasses import dataclass, asdict

@dataclass
class HorseInfoDTO:
    id: str
    name: str
    sex: str
    image: str
    father: str
    grandfather: str
    title: str
    def to_dict(self):
        return asdict(self)
