"""Core implementation for parsing duration strings and sleeping."""

from __future__ import annotations

import re
import time

__all__ = ["DurationError", "parse_duration", "sleep_for"]


class DurationError(ValueError):
    """Raised when a duration string cannot be parsed."""


# One ASCII letter, optional. Whitespace and trailing partial tokens are rejected.
# A bare number is interpreted as seconds (the SI base unit for time).
_UNIT_PATTERN = re.compile(
    r"\A([0-9]+(?:\.[0-9]+)?)\s*([a-z]?)\Z",
    re.IGNORECASE,
)

# Map of unit-letter -> multiplier to seconds. Excludes 'd' (day), 'h' (hour)
# on purpose: a small, unambiguous alphabet is more robust than guessing.
_FACTORS = {
    "":   1.0,
    "s":  1.0,
    "ms": 0.001,
    "m":  60.0,
    "h":  3600.0,
    "d":  86400.0,
}


def parse_duration(text: str) -> float:
    """Parse a duration string like ``'5s'`` or ``'2m'`` into seconds.

    Supported units (single ASCII letter, case-insensitive):
      ``s`` seconds, ``m`` minutes, ``h`` hours, ``d`` days.
    A bare number is interpreted as seconds.

    Raises:
        DurationError: if *text* is not a string, is empty, contains
            an unknown unit, or represents a negative value.
    """
    if not isinstance(text, str):
        raise DurationError(f"duration must be a string, got {type(text).__name__}")

    stripped = text.strip()
    if not stripped:
        raise DurationError("duration string is empty")

    match = _UNIT_PATTERN.match(stripped)
    if match is None:
        raise DurationError(f"invalid duration: {text!r}")

    number_part, unit_part = match.group(1), match.group(2).lower()

    # Reject trailing letters we don't recognise, even when the number is valid.
    # This keeps the alphabet tight and the error message specific.
    if unit_part not in _FACTORS:
        raise DurationError(f"unknown unit {unit_part!r} in duration {text!r}")

    value = float(number_part)
    if value < 0:
        raise DurationError(f"duration must be non-negative, got {value}")

    return value * _FACTORS[unit_part]


def sleep_for(text: str) -> float:
    """Parse *text* and suspend execution for that many seconds.

    Returns the number of seconds actually slept (as requested). The value
    is what was passed to :func:`time.sleep`; wall-clock precision is the
    OS's business, not ours.
    """
    seconds = parse_duration(text)
    time.sleep(seconds)
    return seconds
