import os
import time
from typing import List, Dict
import unittest

import numpy as np

from .morse_code_units import MorseCodeUnits
from .morse_letters import morse_units_to_letter, MORSE_LETTERS
from .morse_code_states import MorseCodeStates
from .morse_state_size import MorseCodeStateSize
from .morse_state_sizes import MorseCodeStateSizes

IS_TEST = 'IS_TEST' in os.environ

DOT = MorseCodeUnits.DOT
DASH = MorseCodeUnits.DASH
SPACE = MorseCodeUnits.SPACE
NEW_LETTER = MorseCodeUnits.NEW_LETTER
NEW_WORD = MorseCodeUnits.NEW_WORD

ACTIVE = MorseCodeStates.ACTIVE
INACTIVE = MorseCodeStates.INACTIVE


def seperate_units_by(morse_units, by=MorseCodeUnits):
    starting_index = 0
    for unit in morse_units:
        if unit != by:
            break
        starting_index += 1
    if len(morse_units) == starting_index:
        return [morse_units]
    units_group = []
    current_group = [morse_units[starting_index]]
    for morse_unit in morse_units[starting_index+1:]:
        if morse_unit != by:
            current_group.append(morse_unit)
        else:
            units_group.append(current_group)
            current_group = []

    if len(current_group) > 0:
        units_group.append(current_group)
    return units_group

def morse_units_to_word(morse_units):
    word = []
    letter_units = seperate_units_by(morse_units, NEW_LETTER)
    for unit in letter_units:
        word.append(morse_units_to_letter(unit))
    
    return ''.join(word)

def morse_units_to_words(morse_units):
    words = []
    word_units = seperate_units_by(morse_units, NEW_WORD)
    for unit in word_units:
        words.append(morse_units_to_word(unit))
    
    return ' '.join(words)

def print_stats(state_sizes):
    output = []
    for e in state_sizes:
        active = 'ON' if e.state == MorseCodeStates.ACTIVE else 'OFF'
        t = e.size
        output.append('{} {}'.format(active, t))
    print(' | '.join(output), end='\r')

def binary_data_to_states_sizes(data: List[int]) -> List[Dict]:
    morse_states_sizes = []
    current_state_size = MorseCodeStateSize(data[0], 1)

    for unit in data[1:]:
        state = MorseCodeStates.value_to_state(unit)
        if state == current_state_size.state:
            # TODO: It's odd to mutate size here
            current_state_size.size += 1
        else:
            morse_states_sizes.append(current_state_size)
            current_state_size = MorseCodeStateSize(unit, 1)
    morse_states_sizes.append(current_state_size)

    return morse_states_sizes

def morse_units_from_state_size(state: MorseCodeStates, size: int):
    if state == MorseCodeStates.ACTIVE:
        if size == 1:
            return MorseCodeUnits.DOT
        if size == 3:
            return MorseCodeUnits.DASH
        # Based on normalization, this is possible
        if size == 7:
            return MorseCodeUnits.DASH
    if state == MorseCodeStates.INACTIVE:
        if size == 1:
            return MorseCodeUnits.SPACE
        if size == 3:
            return MorseCodeUnits.NEW_LETTER
        if size == 7:
            return MorseCodeUnits.NEW_WORD
    
    return None

def state_sizes_to_morse_units(state_sizes):
    morse_units = []
    for state_size in state_sizes:
        state = state_size.state
        size = state_size.size

        unit = morse_units_from_state_size(state, size)
        morse_units.append(unit)
    return morse_units

class MorseCode:
    t = None
    events = None
    normalized_events = None
    def __init__(self) -> None:
        self.t = time.time() #reading time in sec
        self.events = MorseCodeStateSizes()
        self.normalized_events = MorseCodeStateSizes()

    def add_event(self, active = False):
        new_time = time.time()
        time_diff = np.round(new_time - self.t, 2)
        self.t = new_time
        e = MorseCodeStateSize(active, time_diff)
        self.events.append(e)

    def normalize_events(self):
        self.normalized_events = self.events.normalize()
    def translate_data(self) -> str:
        self.normalize_events()
        units = state_sizes_to_morse_units(self.normalized_events)
        words = morse_units_to_words(units)

        return words


class TestMorseCode(unittest.TestCase):
    # TODO: Raw data should have units associated already?
    LETTER_A_RAW = [1, 0, 1, 1, 1]
    LETTER_E_RAW = [1]
    LETTER_T_RAW = [1, 1, 1]
    LETTER_A_STATE_SIZES = None
    WORD_EAT_UNITS = None
    WORD_TEA_UNITS = None
    def setUp(self) -> None:
        self.LETTER_A_STATE_SIZES = [
            MorseCodeStateSize(1, 1),
            MorseCodeStateSize(0, 1),
            MorseCodeStateSize(1, 3),
        ]

        self.WORD_EAT_UNITS = self.helper_create_word('EAT')
        self.WORD_TEA_UNITS = self.helper_create_word('TEA')

        return super().setUp()
    
    def helper_create_word(self, letters: str):
        word = []
        for letter in letters:
            word += MORSE_LETTERS[letter] + [NEW_LETTER]
        return word[:-1] # Remove last NEW_LINE
    
    def test_morse_code_add_event(self):
        morse_code = MorseCode()
        morse_code.add_event(active=True)

        self.assertEqual(len(morse_code.events), 1)
        self.assertEqual(morse_code.events[0], MorseCodeStateSize(1, 0))

    def test_binary_data_to_states_sizes(self):
        data = self.LETTER_A_RAW

        expected_state_sizes = self.LETTER_A_STATE_SIZES

        morse_states_sizes = binary_data_to_states_sizes(data)
        self.assertEqual(morse_states_sizes, expected_state_sizes)
    
    def test_state_sizes_to_morse_units(self):
        state_sizes = self.LETTER_A_STATE_SIZES
        expected_morse = MORSE_LETTERS['A']

        morse_units = state_sizes_to_morse_units(state_sizes)
        self.assertEqual(morse_units, expected_morse)
    
    def test_morse_units_to_letter_a(self):
        morse_units = MORSE_LETTERS['A']
        expected_letter = 'A'

        found_letter = morse_units_to_letter(morse_units)
        self.assertEqual(found_letter, expected_letter)
    
    def test_morse_units_to_letter_e(self):
        morse_units = MORSE_LETTERS['E']
        expected_letter = 'E'

        found_letter = morse_units_to_letter(morse_units)
        self.assertEqual(found_letter, expected_letter)
    
    def test_seperate_units_by_letters(self):
        morse_units = self.WORD_EAT_UNITS
        expected_output = [
            MORSE_LETTERS['E'],
            MORSE_LETTERS['A'],
            MORSE_LETTERS['T']
        ]

        found_units = seperate_units_by(morse_units, NEW_LETTER)
        self.assertEqual(found_units, expected_output)

    def test_seperate_units_by_words(self):
        morse_units = MORSE_LETTERS['E'] + \
            [NEW_WORD] + \
            MORSE_LETTERS['T']
        expected_output = [
            MORSE_LETTERS['E'],
            MORSE_LETTERS['T']
        ]

        found_units = seperate_units_by(morse_units, NEW_WORD)
        self.assertEqual(found_units, expected_output)

    def test_seperate_units_by_words_ignores_extra_newword_boundaries(self):
        morse_units = [NEW_WORD] + \
            MORSE_LETTERS['E'] + \
                [NEW_WORD]

        expected_output = [
            MORSE_LETTERS['E']
        ]

        found_units = seperate_units_by(morse_units, NEW_WORD)
        self.assertEqual(found_units, expected_output)

    def test_morse_units_to_word(self):
        morse_units = self.WORD_EAT_UNITS
        expected_word = 'EAT'

        found_word = morse_units_to_word(morse_units)
        self.assertEqual(found_word, expected_word)

    def test_morse_units_to_words(self):
        morse_units = self.WORD_EAT_UNITS + [NEW_WORD] + self.WORD_TEA_UNITS
        expected_words = 'EAT TEA'

        found_word = morse_units_to_words(morse_units)
        self.assertEqual(found_word, expected_words)

if __name__ == '__main__':
    unittest.main()