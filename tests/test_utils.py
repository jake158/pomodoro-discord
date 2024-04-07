import unittest
from src.utils import load_config, save_config, load_data, save_data


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.saved_config = load_config()
        self.saved_data = load_data()

    def tearDown(self):
        save_config(self.saved_config)
        save_data(self.saved_data)

    def test_load_config(self):
        config = load_config()
        self.assertIsInstance(config, dict)
        self.assertIn('theme', config)
        self.assertIn('sound', config)

    def test_save_config(self):
        config = {'theme': 'test_theme', 'sound': 'test_sound.mp3'}
        save_config(config)
        loaded_config = load_config()
        self.assertEqual(config, loaded_config)

    def test_load_data(self):
        data = load_data()
        self.assertIsInstance(data, dict)
        self.assertIn('total_seconds_studied', data)
        self.assertIn('total_pomodoro_sessions', data)

    def test_save_data(self):
        data = {'total_seconds_studied': 1000, 'total_pomodoro_sessions': 10}
        save_data(data)
        loaded_data = load_data()
        self.assertEqual(data, loaded_data)
