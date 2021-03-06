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
    state_sizes_by_state = None

    # if state_sizes is provided, then a deep copy is made
    def __init__(self, state_sizes: List[MorseCodeStateSize] = None) -> None:
        self.sizes = []
        self.state_sizes_by_state = {
            ACTIVE: [],
            INACTIVE: []
        }
        if state_sizes is not None:
            self.copy_from(state_sizes)

    def copy_from(self, state_sizes):
        for state_size in state_sizes:
            self.append(state_size.copy())
    
    def append(self, state_size: MorseCodeStateSize) -> None:
        size = state_size.size
        self.sizes.append(size)

        state = state_size.state
        self.state_sizes_by_state[state].append(state_size)

        return super().append(state_size)
    
    def normalize(self):
        stats_by_state = {}
        for state in self.state_sizes_by_state:
            state_sizes = self.state_sizes_by_state[state]
            sizes = [state_size.size for state_size in state_sizes]
            if len(sizes):
                std = np.std(sizes)
                stats_by_state[state] = {
                    'smallest': np.min(sizes),
                    'sizes': cap_sizes(sizes),
                    'middle': np.median(sizes),
                    'std': std,
                    'half_std': std / 2
                }

        normalized_state_sizes = MorseCodeStateSizes()
        for state_size in self:
            state = state_size.state
            size = state_size.size
            value = state_size.value

            stats = stats_by_state[state]

            if size < (stats['smallest'] * 1.5):
                size = 1
            elif size < (stats['smallest'] * 4):
                size = 3
            else:
                size = 7
            normalized_state_sizes.append(MorseCodeStateSize(value, size))

        return normalized_state_sizes

    def __repr__(self) -> str:
        output = []
        for state_size in self:
            output.append(str(state_size))
        
        return ', '.join(output)

    @classmethod
    def deserialize(self, serialized_str: str):
        state_sizes = MorseCodeStateSizes()
        for _str in serialized_str.split(', '):
            state, size = _str.split(' ')
            state_size = MorseCodeStateSize(int(state), float(size))
            state_sizes.append(state_size)
        
        return state_sizes



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
            active = abs(active - 1)
        
        return state_sizes

    def test_normalize_sizes(self):
        raw = self.helper_sizes_to_state_sizes([0.2, 0.9, 0.6])
        expected_normalized = self.helper_sizes_to_state_sizes([1, 1, 3])
        normalized = raw.normalize()
        self.assertEqual(normalized, expected_normalized)
        
        raw = self.helper_sizes_to_state_sizes([0.3, 0.7, 1.2])
        expected_normalized = self.helper_sizes_to_state_sizes([1, 1, 7])
        normalized = raw.normalize()
        self.assertEqual(normalized, expected_normalized)
    
    def test_normalize_sizes_extreme(self):
        # Last value should not skew smaller numbers
        raw = self.helper_sizes_to_state_sizes([1, 3, 3, 5, 200])
        expected_normalized = self.helper_sizes_to_state_sizes([1, 1, 3, 3, 7])
        normalized = raw.normalize()
        self.assertEqual(normalized, expected_normalized)
    
    def test_deserialize(self):
        serialized_text = '0 1, 1 3, 0 3'
        _sz = MorseCodeStateSize
        expected_output = MorseCodeStateSizes([_sz(0, 1), _sz(1, 3), _sz(0, 3)])

        state_sizes = MorseCodeStateSizes.deserialize(serialized_text)

        self.assertEqual(state_sizes, expected_output)
