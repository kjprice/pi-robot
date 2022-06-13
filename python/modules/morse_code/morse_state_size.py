import unittest

from .morse_code_states import MorseCodeStates

class MorseCodeStateSize():
    state = None
    size = None
    def __init__(self, value: float, size: float) -> None:
        self.state = MorseCodeStates.value_to_state(value)
        self.size = size
    
    def __eq__(self, __o: object) -> bool:
        return self.state == __o.state and self.size == __o.size

class TestMorseCodeStateSize(unittest.TestCase):
    def test_simple_state_size(self):
        state_size = MorseCodeStateSize(1, 3)
        
        self.assertEqual(state_size.state, MorseCodeStates.ACTIVE)
        self.assertEqual(state_size.size, 3)