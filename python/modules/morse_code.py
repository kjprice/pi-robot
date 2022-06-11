from enum import Enum
import os
import unittest

IS_TEST = 'IS_TEST' in os.environ

class MorseCodeUnits(Enum):
    DOT = 1
    DASH = 2
    SPACE = 3
    NEW_LETTER = 4
    NEW_WORD = 5

DOT = MorseCodeUnits.DOT
DASH = MorseCodeUnits.DASH
SPACE = MorseCodeUnits.SPACE

class MorseCodeStates(Enum):
    ACTIVE = 1
    INACTIVE = 2

    @classmethod
    def value_to_state(self, value):
        if value == 0:
            return self.INACTIVE
        return self.ACTIVE

ACTIVE = MorseCodeStates.ACTIVE
INACTIVE = MorseCodeStates.INACTIVE

MORSE_LETTERS = {
    'A': [DOT, SPACE, DASH],
    'E': [DOT],
    'T': [DASH],
}

def morse_units_to_letter(morse_units):
    # TODO: Inneficient - maybe use a trie?
    for letter in MORSE_LETTERS:
        units = MORSE_LETTERS[letter]
        if morse_units == units:
            return letter

def data_to_states_counts(data):
    morse_states_counts = []
    current_state_count = {
        'state': MorseCodeStates.value_to_state(data[0]),
        'count': 1
    }

    for unit in data[1:]:
        state = MorseCodeStates.value_to_state(unit)
        if state == current_state_count['state']:
            current_state_count['count'] += 1
        else:
            morse_states_counts.append(current_state_count)
            current_state_count = {
                'state': MorseCodeStates.value_to_state(unit),
                'count': 1
            }
    morse_states_counts.append(current_state_count)

    return morse_states_counts

def morse_units_from_state_count(state, count):
    if state == MorseCodeStates.ACTIVE:
        if count == 1:
            return MorseCodeUnits.DOT
        if count == 3:
            return MorseCodeUnits.DASH
    if state == MorseCodeStates.INACTIVE:
        if count == 1:
            return MorseCodeUnits.SPACE
        if count == 3:
            return MorseCodeUnits.NEW_LETTER
        if count == 7:
            return MorseCodeUnits.NEW_WORD
    
    return None

def state_counts_to_morse_units(state_counts):
    morse_units = []
    for state_count in state_counts:
        state = state_count['state']
        count = state_count['count']

        unit = morse_units_from_state_count(state, count)
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
    LETTER_A_RAW = [1, 0, 1, 1, 1]
    LETTER_E_RAW = [1]
    LETTER_T_RAW = [1, 1, 1]
    LETTER_A_STATE_COUNTS = None
    def setUp(self) -> None:
        self.LETTER_A_STATE_COUNTS = self.helper_get_state_counts([
            [ACTIVE, 1],
            [INACTIVE, 1],
            [ACTIVE, 3],
        ])
        return super().setUp()
    
    def helper_get_state_count(self, state: MorseCodeStates, count):
        return {
            'state': state,
            'count': count
        }
    
    def helper_get_state_counts(self, state_counts):
        output = []
        for state_count in state_counts:
            state, count = state_count
            output.append(self.helper_get_state_count(state, count))
        return output

    def test_data_to_states_counts(self):
        data = self.LETTER_A_RAW

        expected_state_counts = self.LETTER_A_STATE_COUNTS

        morse_states_counts = data_to_states_counts(data)
        self.assertEqual(morse_states_counts, expected_state_counts)
    
    def test_state_counts_to_morse_units(self):
        state_counts = self.LETTER_A_STATE_COUNTS
        expected_morse = MORSE_LETTERS['A']

        morse_units = state_counts_to_morse_units(state_counts)
        self.assertEqual(morse_units, expected_morse)
    
    def test_morse_units_to_letter(self):
        morse_units = MORSE_LETTERS['A']
        expected_letter = 'A'

        found_letter = morse_units_to_letter(morse_units)
        self.assertEqual(found_letter, expected_letter)

# TODO:
# - test with a word
# - test with two words
# - include variance in units...round to nearest odd number
# - include odd units - resize so smallest unit is 1
# - include variance of values - turn 0.7 into 1 for example based on context

if IS_TEST:
    unittest.main()