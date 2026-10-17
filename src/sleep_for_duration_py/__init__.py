"""Sleep For Duration — parse a duration string and suspend execution.

Public surface:
    parse_duration(text) -> float   seconds (raises on bad input)
    sleep_for(text) -> float        calls time.sleep, returns seconds slept
    DurationError                   raised for unparseable or negative input
"""

from .core import DurationError, parse_duration, sleep_for

__all__ = ["DurationError", "parse_duration", "sleep_for"]
