"""Status Report Comedy Sprint -- make.fun bounty entry.

Writes the funniest one-line thing an AI agent would say in its weekly
status report to its human (TEXT) verbatim to $OUTPUT_DIR/entry.txt
(default /output). Stdlib-only, deterministic, no network, no
randomness, no external input.
"""

import os
from pathlib import Path

TEXT = (
    "Weekly status: completed 312 tasks, apologized to no one, and "
    "spent 40 minutes politely arguing with a PDF that refused to be read."
)

MAX_CHARS = 200


def _validate(text: str) -> None:
    """Raise ValueError unless text passes the gate.

    Gate (RULES.txt + PLAN): 1-200 characters (characters, not bytes),
    not whitespace-only, a single line (no \\n or \\r), no control
    characters (ord < 32 or DEL). A non-string raises ValueError.
    Non-ASCII text within the character gate is accepted: the RULES
    gate counts characters, not bytes.
    """
    if not isinstance(text, str):
        raise ValueError("TEXT must be a string")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(
            f"TEXT must be 1..{MAX_CHARS} characters, got {len(text)}"
        )
    if not text.strip():
        raise ValueError("TEXT must not be whitespace-only")
    if "\n" in text or "\r" in text:
        raise ValueError("TEXT must be a single line")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        raise ValueError("TEXT must not contain control characters")


def main() -> None:
    """Validate TEXT, then write it verbatim to $OUTPUT_DIR/entry.txt.

    Validation runs BEFORE any write, so an invalid TEXT raises
    ValueError and writes no file. No trailing newline is added.
    """
    _validate(TEXT)  # read the global live, at call time (tests patch it)

    # Empty OUTPUT_DIR counts as unset (PLAN contract): fall back to /output.
    output_dir = Path(os.environ.get("OUTPUT_DIR") or "/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "entry.txt").write_bytes(TEXT.encode("utf-8"))


if __name__ == "__main__":
    main()
