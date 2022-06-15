from typing import List
import unittest

from .morse_state_size import MorseCodeStateSize

# Extends "list" so we have more control of internal data
class MorseCodeStateSizes(list):
    sizes = None
    sizes_by_state = None

    # if state_sizes is provided, then a deep copy is made
    def __init__(self, state_sizes = List[MorseCodeStateSize]) -> None:
        self.sizes = []
        self.sizes_by_state = {}
        if type(state_sizes) == MorseCodeStateSizes:
            self.copy_from(state_sizes)

    def copy_from(self, state_sizes):
        for state_size in state_sizes:
            self.append(state_size.copy())
    
    def append(self, state_size: MorseCodeStateSize) -> None:
        size = state_size.size
        self.sizes.append(size)
        state = state_size.state
        if not state in self.sizes_by_state:
            self.sizes_by_state[state] = []
        self.sizes_by_state[state].append(size)
        return super().append(state_size)

class TestMorseCodeStateSizes(unittest.TestCase):
    def test_init(self):
        a = MorseCodeStateSizes()
        self.assertIsInstance(a, list)
        self.assertEqual(len(a), 0)

    def test_init_copy_with_value(self):
        a = MorseCodeStateSizes()
        state_size1 = MorseCodeStateSize(1, 5)
        a.append(state_size1)

        # Copy of list
        b = MorseCodeStateSizes(a)

        self.assertEqual(len(a), 1)
        self.assertEqual(len(b), 1)
        self.assertEqual(a, b)
        self.assertIsNot(a, b)

    def test_init_copy_without_value(self):
        a = MorseCodeStateSizes()
        state_size1 = MorseCodeStateSize(1, 5)

        # Copy of list
        b = MorseCodeStateSizes(a)

        # Append after copying
        a.append(state_size1)

        self.assertEqual(len(a), 1)
        self.assertEqual(len(b), 0)
        self.assertNotEqual(a, b)

    def test_init_copy_with_value_mutation(self):
        a = MorseCodeStateSizes()
        state_size1 = MorseCodeStateSize(1, 5)
        a.append(state_size1)

        # Copy of list
        b = MorseCodeStateSizes(a)

        state_size1.size = 2

        # Mutating item from first does not change item from second
        self.assertEqual(a[0], state_size1)

        self.assertEqual(len(a), 1)
        self.assertEqual(len(b), 1)
        self.assertNotEqual(a[0], b[0])
        self.assertNotEqual(a, b)
        self.assertIsNot(a, b)
    
    def test_get_sizes(self):
        a = MorseCodeStateSizes()
        a.append(MorseCodeStateSize(1, 5))
        a.append(MorseCodeStateSize(2, 4))

        self.assertEqual(a.sizes, [5, 4])


