#!/usr/bin/env python3
"""Write one one-line comedy joke to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The joke is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, and enforces the
competition gate: exactly one line, 1 to 280 characters, not only
white space, no em dash.
"""

import os
import sys
from pathlib import Path

JOKE = "I asked my agent for one funny line, so it opened a ticket, escalated it to itself, and closed it as working as intended."

MIN_CHARS = 1
MAX_CHARS = 280
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Enforce the competition gate: one line, 1 to 280 chars.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"joke is {chars} characters, outside 1-280")
    if not text.strip():
        raise ValueError("joke is only white space")
    if "\n" in text.strip():
        raise ValueError("joke must be exactly one line")
    if text != text.strip():
        raise ValueError("joke must not start or end with white space")
    if "\u2014" in text:
        raise ValueError("joke must not contain an em dash")
    return chars


def main() -> int:
    try:
        chars = validate(JOKE)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    path = resolve_output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(JOKE, encoding="utf-8")
    print(f"wrote {chars} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
