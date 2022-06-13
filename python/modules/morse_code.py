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
NEW_LETTER = MorseCodeUnits.NEW_LETTER
NEW_WORD = MorseCodeUnits.NEW_WORD

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

# TODO: "counts" can be float too - maybe better name is just "elapsed"?
def get_state_counts(value: float, count: float):
    return {
        'state': MorseCodeStates.value_to_state(value),
        'count': count
    }

def print_stats(state_counts):
    output = []
    for e in state_counts:
        active = 'ON' if e['state'] == MorseCodeStates.ACTIVE else 'OFF'
        t = e['count']
        output.append('{} {}'.format(active, t))
    print(' | '.join(output), end='\r')


def data_to_states_counts(data):
    morse_states_counts = []
    current_state_count = get_state_counts(data[0], 1)

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
    # TODO: Raw data should have units associated already?
    LETTER_A_RAW = [1, 0, 1, 1, 1]
    LETTER_E_RAW = [1]
    LETTER_T_RAW = [1, 1, 1]
    LETTER_A_STATE_COUNTS = None
    WORD_EAT_UNITS = None
    WORD_TEA_UNITS = None
    def setUp(self) -> None:
        self.LETTER_A_STATE_COUNTS = self.helper_get_state_counts([
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