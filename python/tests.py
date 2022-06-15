import unittest
from .modules.morse_code.morse_code import TestMorseCode
from .modules.morse_code.morse_state_size import TestMorseCodeStateSize
from .modules.morse_code.morse_state_sizes import TestMorseCodeStateSizes
from .modules.morse_code.morse_letters import TestMorseLetters

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestMorseCode))
suite.addTest(unittest.makeSuite(TestMorseCodeStateSize))
suite.addTest(unittest.makeSuite(TestMorseCodeStateSizes))
suite.addTest(unittest.makeSuite(TestMorseLetters))

runner = unittest.TextTestRunner()
runner.run(suite)
