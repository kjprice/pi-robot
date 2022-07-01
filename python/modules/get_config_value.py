import argparse
import json
import unittest
from .config import load_json_config

def get_config_value(config, keys_str: str):
    keys = keys_str.split('.')
    value = config
    for key in keys:
        value = value[key]
    return value

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Provides a config value based on keys represented in dot notation')
    parser.add_argument('-k','--keys', help='keys to traverse through config (example "logs.webminPort")', required=True)
    args = parser.parse_args()

    config = load_json_config()
    value = get_config_value(config, args.keys)
    print(value)

class TestGetConfigValue(unittest.TestCase):
    config_for_testing = None
    def setUp(self) -> None:
        self.config_for_testing = {
            'ports': {
                'test_port': 123
            }
        }
        return super().setUp()
    def test_get_config_value_port(self):
        config = self.config_for_testing
        value = get_config_value(config, 'ports.test_port')
        self.assertEqual(value, 123)

