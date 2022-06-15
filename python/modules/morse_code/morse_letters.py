from typing import List
import unittest

from .morse_code_units import MorseCodeUnits

DOT = MorseCodeUnits.DOT
DASH = MorseCodeUnits.DASH
SPACE = MorseCodeUnits.SPACE

def add_spaces(units: List[MorseCodeUnits]) -> List[MorseCodeUnits]:
    units_with_spaces = []
    for unit in units:
        if len(units_with_spaces) != 0:
            units_with_spaces.append(SPACE)
        units_with_spaces.append(unit)
    
    return units_with_spaces

MORSE_LETTERS = {
    'A': add_spaces([DOT, DASH]),
    'B': add_spaces([DASH, DOT, DOT, DOT]),
    'C': add_spaces([DASH, DOT, DASH, DOT]),
    'D': add_spaces([DASH, DOT, DOT]),
    'E': [DOT],
    'F': add_spaces([DOT, DOT, DASH, DOT]),
    'G': add_spaces([DASH, DASH, DOT]),
    'H': add_spaces([DOT, DOT, DOT, DOT]),
    'I': add_spaces([DOT, DOT]),
    'J': add_spaces([DOT, DASH, DASH, DASH]),
    'K': add_spaces([DASH, DOT, DASH]),
    'L': add_spaces([DOT, DASH, DOT, DOT]),
    'M': add_spaces([DASH, DASH]),
    'N': add_spaces([DASH, DOT]),
    'O': add_spaces([DASH, DASH, DASH]),
    'P': add_spaces([DOT, DASH, DASH, DOT]),
    'Q': add_spaces([DASH, DASH, DOT, DASH]),
    'R': add_spaces([DOT, DASH, DOT]),
    'S': add_spaces([DOT, DOT, DOT]),
    'T': [DASH],
    'U': add_spaces([DOT, DOT, DASH]),
    'V': add_spaces([DOT, DOT, DOT, DASH]),
    'W': add_spaces([DOT, DASH, DASH]),
    'X': add_spaces([DASH, DOT, DOT, DASH]),
    'Y': add_spaces([DASH, DOT, DASH, DASH]),
    'Z': add_spaces([DASH, DASH, DOT, DOT]),
}

# Turns List[MorseCodeUnits] into a string of their values
def serialize_units(units):
    output = []
    for unit in units:
        output.append(unit.value)
    
    return '_'.join(output)

MORSE_UNITS_TO_LETTER = {}
for letter in MORSE_LETTERS:
    units = MORSE_LETTERS[letter]
    units_str = serialize_units(units)
    MORSE_UNITS_TO_LETTER[units_str] = letter

def morse_units_to_letter(morse_units):
    units_str = serialize_units(morse_units)
    if units_str in MORSE_UNITS_TO_LETTER:
        return MORSE_UNITS_TO_LETTER[units_str]
    
    return '?'

class TestMorseLetters(unittest.TestCase):
    def test_add_spaces(self):
        input = [DOT, DASH]
        expected_output = [DOT, SPACE, DASH]

        output = add_spaces(input)

        self.assertEqual(output, expected_output)
        self.assertEqual(output, MORSE_LETTERS['A'])

    def test_morse_letters_dict(self):
        self.assertEqual(len(MORSE_LETTERS), 26)

    def test_morse_units_to_letters_dict(self):
        self.assertEqual(len(MORSE_UNITS_TO_LETTER), 26)

        letters_from_units = list(MORSE_UNITS_TO_LETTER.values())
        letters_keys = list(MORSE_LETTERS.keys())
        
        self.assertEqual(letters_from_units, letters_keys)
