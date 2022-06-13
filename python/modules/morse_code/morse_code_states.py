from enum import Enum

class MorseCodeStates(Enum):
    ACTIVE = 1
    INACTIVE = 2

    @classmethod
    def value_to_state(self, value):
        if value == 0:
            return self.INACTIVE
        return self.ACTIVE
