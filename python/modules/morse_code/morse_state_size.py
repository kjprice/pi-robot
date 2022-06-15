import unittest

from .morse_code_states import MorseCodeStates

class MorseCodeStateSize():
    value = None
    state = None
    size = None
    
    def __init__(self, value: float, size: float) -> None:
        self.value = value
        self.state = MorseCodeStates.value_to_state(value)
        self.size = size
    
    def copy(self):
        return MorseCodeStateSize(self.value, self.size)

    def __eq__(self, __o: object) -> bool:
        return self.state == __o.state and self.size == __o.size
    
    def __repr__(self) -> str:
        state = '1' if self.state == MorseCodeStates.ACTIVE else '0'
        return '{} {}'.format(state, self.size)

class TestMorseCodeStateSize(unittest.TestCase):
    def test_simple_state_size(self):
        state_size = MorseCodeStateSize(1, 3)
        
        self.assertEqual(state_size.state, MorseCodeStates.ACTIVE)
        self.assertEqual(state_size.size, 3)
    
    def test_copy(self):
        state_size1 = MorseCodeStateSize(1, 3)
        state_size2 = state_size1.copy()
        self.assertEqual(state_size1, state_size2)
        self.assertIsNot(state_size1, state_size2)
