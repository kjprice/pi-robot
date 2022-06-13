import os
from typing import List, Dict
import unittest

from .morse_code_units import MorseCodeUnits
from .morse_letters import morse_units_to_letter, MORSE_LETTERS
from .morse_code_states import MorseCodeStates, to_state_size

IS_TEST = 'IS_TEST' in os.environ

DOT = MorseCodeUnits.DOT
DASH = MorseCodeUnits.DASH
SPACE = MorseCodeUnits.SPACE
NEW_LETTER = MorseCodeUnits.NEW_LETTER
NEW_WORD = MorseCodeUnits.NEW_WORD

ACTIVE = MorseCodeStates.ACTIVE
INACTIVE = MorseCodeStates.INACTIVE

def seperate_units_by(morse_units, by=MorseCodeUnits):
    units_group = []
    current_group = [morse_units[0]]
    for morse_unit in morse_units[1:]:
        if morse_unit != by:
            current_group.append(morse_unit)
        else:
            units_group.append(current_group)
            current_group = []

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
        active = 'ON' if e['state'] == MorseCodeStates.ACTIVE else 'OFF'
        t = e['size']
        output.append('{} {}'.format(active, t))
    print(' | '.join(output), end='\r')

def binary_data_to_states_sizes(data: List[int]) -> List[Dict]:
    morse_states_sizes = []
    current_state_size = to_state_size(data[0], 1)

    for unit in data[1:]:
        state = MorseCodeStates.value_to_state(unit)
        if state == current_state_size['state']:
            current_state_size['size'] += 1
        else:
            morse_states_sizes.append(current_state_size)
            current_state_size = to_state_size(unit, 1)
    morse_states_sizes.append(current_state_size)

    return morse_states_sizes

def morse_units_from_state_size(state, size):
    if state == MorseCodeStates.ACTIVE:
        if size == 1:
            return MorseCodeUnits.DOT
        if size == 3:
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
        state = state_size['state']
        size = state_size['size']

        unit = morse_units_from_state_size(state, size)
        morse_units.append(unit)
    return morse_units

class MorseCode:
    raw_data = None
    def __init__(self) -> None:
        self.raw_data = []
    def translate_data(self):
        pass

    def raw_data_to_morse(self):
        # pass
        morse_units = []


class TestMorseCode(unittest.TestCase):
    # TODO: Raw data should have units associated already?
    LETTER_A_RAW = [1, 0, 1, 1, 1]
    LETTER_E_RAW = [1]
    LETTER_T_RAW = [1, 1, 1]
    LETTER_A_STATE_SIZES = None
    WORD_EAT_UNITS = None
    WORD_TEA_UNITS = None
    def setUp(self) -> None:
        self.LETTER_A_STATE_SIZES = self.helper_get_state_sizes([
            [ACTIVE, 1],
            [INACTIVE, 1],
            [ACTIVE, 3],
        ])

        self.WORD_EAT_UNITS = self.helper_create_word('EAT')
        self.WORD_TEA_UNITS = self.helper_create_word('TEA')

        return super().setUp()
    
    def helper_create_word(self, letters: str):
        word = []
        for letter in letters:
            word += MORSE_LETTERS[letter] + [NEW_LETTER]
        return word[:-1] # Remove last NEW_LINE
    def helper_get_state_size(self, state: MorseCodeStates, size):
        return {
            'state': state,
            'size': size
        }
    
    def helper_get_state_sizes(self, state_sizes):
        output = []
        for state_size in state_sizes:
            state, size = state_size
            output.append(self.helper_get_state_size(state, size))
        return output

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
    
    def test_morse_units_to_letter(self):
        morse_units = MORSE_LETTERS['A']
        expected_letter = 'A'

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

# TODO:
# - include variance in units...round to nearest odd number
# - include odd units - resize so smallest unit is 1
# - include variance of values - turn 0.7 into 1 for example based on context

if __name__ == '__main__':
    unittest.main()