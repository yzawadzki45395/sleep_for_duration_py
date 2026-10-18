# sleep_for_duration_py

Parses a duration string like `5s` or `2m` and suspends execution for that long.

```python
from sleep_for_duration_py import parse_duration, sleep_for, DurationError

seconds = parse_duration("2m")   # 120.0
sleep_for("5s")                   # blocks for 5 seconds, returns 5.0
```

## Why

`time.sleep(5)` is fine when you already have seconds. The moment a config
file or CLI flag wants `30m`, you end up with half a parser scattered across
your codebase. This library is that parser, distilled.

Supported units (single ASCII letter, case-insensitive): `s` seconds, `m`
minutes, `h` hours, `d` days. A bare number is interpreted as seconds.

## Edge cases

- Only single-letter units are accepted. `5ms` is rejected — use `0.005s`.
- Negative durations raise `DurationError`; `time.sleep` would also reject
  them, but we surface the error at parse time before touching the clock.
- Trailing garbage like `5s5` raises rather than silently taking the first
  token.
