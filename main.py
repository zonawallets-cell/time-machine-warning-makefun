"""Funniest Time Machine Warning Label — make.fun entry.

A tiny program that writes the time machine's warning label, one line,
to the entry file the grader reads: $MAKEFUN_OUTPUT_DIR/entry.txt
(or /output/entry.txt when the variable is unset).

The label itself is a fixed string. Nothing is fetched, generated, or
randomised at run time; the program only validates the string against
the competition gate and writes it out.

Standard library only: os.
"""

import os

LINE = "NOTICE: Passengers who kill their grandfather will be charged a cleaning fee."

MAX_CHARS = 120


def check_gate(text):
    """Reject anything the competition gate would reject.

    The gate wants UTF-8 text of 1-120 characters, a single line, and
    more than whitespace. Anything else raises ValueError.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if len(text) < 1 or len(text) > MAX_CHARS:
        raise ValueError("entry must be 1-%d characters, got %d"
                         % (MAX_CHARS, len(text)))
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    text.encode("utf-8")


def write_entry(text):
    """Validate the line, write it, then read it back to prove the
    file on disk is exactly the line the gate checked."""
    check_gate(text)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    with open(path, "r", encoding="utf-8", newline="") as handle:
        on_disk = handle.read()
    if on_disk != text:
        raise ValueError("entry.txt does not match the validated line")
    return path


def main():
    path = write_entry(LINE)
    print("wrote %d chars to %s (verified)" % (len(LINE), path))


if __name__ == "__main__":
    main()
