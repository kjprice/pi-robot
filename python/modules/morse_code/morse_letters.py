from .morse_code_units import MorseCodeUnits

DOT = MorseCodeUnits.DOT
DASH = MorseCodeUnits.DASH
SPACE = MorseCodeUnits.SPACE

MORSE_LETTERS = {
    'A': [DOT, SPACE, DASH],
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
    return MORSE_UNITS_TO_LETTER[units_str]
