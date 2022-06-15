from typing import List

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
    'E': [DOT],
    'T': [DASH],
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
