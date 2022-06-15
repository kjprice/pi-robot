from typing import List
import unittest

import numpy as np

from .morse_state_size import MorseCodeStateSize
from .morse_code_states import MorseCodeStates

ACTIVE = MorseCodeStates.ACTIVE
INACTIVE = MorseCodeStates.INACTIVE

def cap_sizes(sizes):
    LARGEST_UNIT = 7
    smallest_number = np.min(sizes)
    largest_allowed_size = smallest_number * LARGEST_UNIT
    capped_sizes =[]
    for size in sizes:
        if size > largest_allowed_size:
            size = largest_allowed_size
        capped_sizes.append(size)
    
    return capped_sizes

# Extends "list" so we have more control of internal data
class MorseCodeStateSizes(list):
    sizes = None
    sizes_by_state = None

    # if state_sizes is provided, then a deep copy is made
    def __init__(self, state_sizes = List[MorseCodeStateSize]) -> None:
        self.sizes = []
        self.sizes_by_state = {
            ACTIVE: [],
            INACTIVE: []
        }
        if type(state_sizes) == MorseCodeStateSizes:
            self.copy_from(state_sizes)

    def copy_from(self, state_sizes):
        for state_size in state_sizes:
            self.append(state_size.copy())
    
    def append(self, state_size: MorseCodeStateSize) -> None:
        size = state_size.size
        self.sizes.append(size)

        state = state_size.state
        self.sizes_by_state[state].append(size)

        return super().append(state_size)
    
    def normalize(self):
        sizes = self.sizes
        sizes = cap_sizes(sizes)
        middle = np.median(sizes)
        std = np.std(sizes)
        half_std = std / 2
        normalized_state_sizes = MorseCodeStateSizes()
        for state_size in self:
            size = state_size.size
            value = state_size.value

            if size < (middle - half_std):
                size = 1
            elif size < (middle + std):
                size = 3
            else:
                size = 7
            normalized_state_sizes.append(MorseCodeStateSize(value, size))

        return normalized_state_sizes

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

    def helper_sizes_to_state_sizes(self, sizes: List[float]):
        state_sizes = MorseCodeStateSizes()
        active = 0
        for size in sizes:
            state_sizes.append(MorseCodeStateSize(active, size))
        
        return state_sizes

    def test_normalize_sizes(self):
        # Does not find any sevens (7) because middle number is so high
        raw = self.helper_sizes_to_state_sizes([0.2, 0.9, 1.2])
        expected_normalized = self.helper_sizes_to_state_sizes([1, 3, 3])
        normalized = raw.normalize()
        self.assertEqual(normalized, expected_normalized)
        
        # The middle number (0.7) changes criterium for what would be a 7
        raw = self.helper_sizes_to_state_sizes([0.3, 0.7, 1.2])
        expected_normalized = self.helper_sizes_to_state_sizes([1, 3, 7])
        normalized = raw.normalize()
        self.assertEqual(normalized, expected_normalized)
    
    def test_normalize_sizes_extreme(self):
        # Last value should not skew smaller numbers
        raw = self.helper_sizes_to_state_sizes([1, 2, 3, 7, 200])
        expected_normalized = self.helper_sizes_to_state_sizes([1, 3, 3, 7, 7])
        normalized = raw.normalize()
        self.assertEqual(normalized, expected_normalized)


