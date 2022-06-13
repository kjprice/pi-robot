import unittest
from .modules.morse_code.morse_code import TestMorseCode
from .modules.morse_code.morse_state_size import TestMorseCodeStateSize

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestMorseCode))
suite.addTest(unittest.makeSuite(TestMorseCodeStateSize))

runner = unittest.TextTestRunner()
runner.run(suite)
