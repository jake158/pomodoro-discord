import warnings
import unittest
from src.frames.pomodoro_frame import PomodoroFrame
from src.utils import load_config, DEF_POMODORO_MINS, DEF_SB_BEFORE_L


def ignore_warnings(test_func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            test_func(self, *args, **kwargs)
    return do_test


class TestPomodoroFrame(unittest.TestCase):

    @ignore_warnings
    def setUp(self):
        self.config = load_config()
        self.pomodoro_frame = PomodoroFrame(None)

    @ignore_warnings
    def test_initialize_ui(self):
        config = self.config
        frame = self.pomodoro_frame
        self.assertIsNotNone(frame)

        self.assertIsNotNone(frame.break_text)
        self.assertEqual(frame.pomodoro_time, config.get("pomodoro_time", DEF_POMODORO_MINS) * 60)
        self.assertIsNotNone(frame.timer_display)
        self.assertIsNotNone(frame.start_button)
        self.assertIsNotNone(frame.start_button)
        self.assertIsNotNone(frame.sb_button)
        self.assertIsNotNone(frame.lb_button)
        self.assertIsNotNone(frame.reset_button)

        self.assertFalse(frame.running)
        self.assertFalse(frame.break_running)
        self.assertIsNone(frame.next_timer_update)
        self.assertEqual(frame.remaining_time, frame.pomodoro_time)

        self.assertEqual(frame.auto_break_cycling, config.get("auto_break_cycling", False))
        self.assertEqual(frame.short_breaks_before_long, config.get("short_breaks_before_long", DEF_SB_BEFORE_L))
        self.assertFalse(frame.short_break_running)
        self.assertEqual(frame.short_break_counter, 0)

        self.assertIsNone(frame.start_time_timestamp)
        self.assertIsNone(frame.end_time_timestamp)

        self.assertEqual(frame.session_counter, 0)
        self.assertEqual(frame.seconds_studied, 0)

    @ignore_warnings
    def test_toggle_timer(self):
        frame = self.pomodoro_frame
        frame.toggle_timer()
        self.assertTrue(frame.running)
        self.assertIsNotNone(frame.start_time_timestamp)
        self.assertIsNotNone(frame.end_time_timestamp)
        frame.toggle_timer()
        self.assertFalse(frame.running)

    @ignore_warnings
    def test_reset(self):
        frame = self.pomodoro_frame
        frame.running = True
        frame.break_running = True
        frame.short_break_running = True
        frame.break_text.set("Short break")
        frame.remaining_time = 100
        frame.reset()
        self.assertFalse(frame.running)
        self.assertFalse(frame.break_running)
        self.assertFalse(frame.short_break_running)
        self.assertEqual(frame.break_text.get(), "")
        self.assertEqual(frame.remaining_time, frame.pomodoro_time)

    @ignore_warnings
    def test_short_break(self):
        frame = self.pomodoro_frame
        frame.short_break()
        self.assertTrue(frame.break_running)
        self.assertTrue(frame.short_break_running)
        self.assertEqual(frame.break_text.get(), "Short break")

    @ignore_warnings
    def test_long_break(self):
        frame = self.pomodoro_frame
        frame.long_break()
        self.assertTrue(frame.break_running)
        self.assertEqual(frame.break_text.get(), "Long break")
