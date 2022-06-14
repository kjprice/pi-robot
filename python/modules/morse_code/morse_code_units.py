from enum import Enum

class MorseCodeUnits(Enum):
    DOT = 'DOT'
    DASH = 'DASH'
    SPACE = 'SPACE'
    NEW_LETTER = 'NEW_LETTER'
    NEW_WORD = 'NEW_WORD'

    def __repr__(self) -> str:
        return self.value