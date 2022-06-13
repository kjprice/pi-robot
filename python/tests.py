import unittest
from .modules.morse_code.morse_code import TestMorseCode

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestMorseCode))

runner = unittest.TextTestRunner()
runner.run(suite)
