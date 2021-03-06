import os
import unittest

os.environ['IS_TEST'] = "true"

from .modules.morse_code.morse_code import TestMorseCode
from .modules.morse_code.morse_state_size import TestMorseCodeStateSize
from .modules.morse_code.morse_state_sizes import TestMorseCodeStateSizes
from .modules.morse_code.morse_letters import TestMorseLetters

from .modules.process_image_for_servo import TestProcessImages
from .modules.servo_module import TestServoModule
from .modules.get_config_value import TestGetConfigValue

# Just make sure that we can import all main code
from .pi_applications import run_camera_detect_morse_code
from .pi_applications import run_camera_head_server
from .pi_applications import run_image_processing_server
from .pi_applications import run_servo_server
from .modules.raspi_info.raspi_poller import RaspiPoller

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestMorseCode))
suite.addTest(unittest.makeSuite(TestMorseCodeStateSize))
suite.addTest(unittest.makeSuite(TestMorseCodeStateSizes))
suite.addTest(unittest.makeSuite(TestMorseLetters))
suite.addTest(unittest.makeSuite(TestProcessImages))
suite.addTest(unittest.makeSuite(TestServoModule))
suite.addTest(unittest.makeSuite(TestGetConfigValue))
runner = unittest.TextTestRunner()
runner.run(suite)
