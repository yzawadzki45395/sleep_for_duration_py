import time
import unittest

from sleep_for_duration_py.core import DurationError, parse_duration, sleep_for


class TestParseDuration(unittest.TestCase):
    def test_seconds(self):
        self.assertEqual(parse_duration("5s"), 5.0)

    def test_bare_number_is_seconds(self):
        self.assertEqual(parse_duration("7"), 7.0)

    def test_minutes(self):
        self.assertEqual(parse_duration("2m"), 120.0)

    def test_hours(self):
        self.assertEqual(parse_duration("1h"), 3600.0)

    def test_days(self):
        self.assertEqual(parse_duration("1d"), 86400.0)

    def test_decimal(self):
        self.assertEqual(parse_duration("1.5"), 1.5)

    def test_uppercase_unit(self):
        self.assertEqual(parse_duration("3M"), 180.0)

    def test_whitespace_around(self):
        self.assertEqual(parse_duration("  5s  "), 5.0)

    def test_empty_raises(self):
        with self.assertRaises(DurationError):
            parse_duration("")

    def test_whitespace_only_raises(self):
        with self.assertRaises(DurationError):
            parse_duration("   ")

    def test_unknown_unit_raises(self):
        with self.assertRaises(DurationError):
            parse_duration("5x")

    def test_negative_raises(self):
        with self.assertRaises(DurationError):
            parse_duration("-5s")

    def test_non_string_raises(self):
        with self.assertRaises(DurationError):
            parse_duration(5)

    def test_trailing_garbage_raises(self):
        with self.assertRaises(DurationError):
            parse_duration("5s5")

    def test_millisecond_unit_rejected(self):
        # Only single-letter units are supported; 'ms' is not a single letter.
        with self.assertRaises(DurationError):
            parse_duration("5ms")


class TestSleepFor(unittest.TestCase):
    """Test parsing and the call to time.sleep without actually waiting."""

    def setUp(self):
        self._real_sleep = time.sleep
        self.calls = []

        def fake_sleep(seconds):
            self.calls.append(seconds)

        time.sleep = fake_sleep

    def tearDown(self):
        time.sleep = self._real_sleep

    def test_sleeps_for_seconds(self):
        result = sleep_for("5s")
        self.assertEqual(result, 5.0)
        self.assertEqual(self.calls, [5.0])

    def test_sleeps_for_minutes(self):
        sleep_for("1m")
        self.assertEqual(self.calls, [60.0])

    def test_bad_input_raises_before_sleep(self):
        with self.assertRaises(DurationError):
            sleep_for("abc")
        self.assertEqual(self.calls, [])


if __name__ == "__main__":
    unittest.main()
