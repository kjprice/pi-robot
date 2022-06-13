from enum import Enum

class MorseCodeStates(Enum):
    ACTIVE = 1
    INACTIVE = 2

    @classmethod
    def value_to_state(self, value):
        if value == 0:
            return self.INACTIVE
        return self.ACTIVE

def to_state_size(value: float, size: float):
    return {
        'state': MorseCodeStates.value_to_state(value),
        'size': size
    }

