"""One fortune for a houseplant, written to /output/entry.txt.

The bounty asks for a single line, at most 120 characters, that tells the
future of the plant on the windowsill: kind, a little funny, and sounding
like a fortune rather than a slogan. This program holds that one line,
checks it against the gate, and writes it out. It never touches the
network and always writes the same bytes.
"""

import os
import sys

LINE = (
    "By Thursday your shadow will reach the teacup, and your keeper will "
    "finally admit the windowsill is yours, not theirs."
)

LIMIT = 120


def check(text):
    """Raise ValueError unless the text satisfies the competition gate."""
    faults = []
    if not text:
        faults.append("entry is empty")
    if len(text) > LIMIT:
        faults.append("entry is %d characters, over the %d limit" % (len(text), LIMIT))
    if "\n" in text or "\r" in text:
        faults.append("entry must be a single line")
    if text != text.strip():
        faults.append("entry must not start or end with white space")
    if text.strip() == "":
        faults.append("entry must not be only white space")
    if faults:
        raise ValueError("; ".join(faults))


def emit(text):
    """Write the line plus a trailing newline and return its path."""
    folder = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "entry.txt")
    handle = open(path, "w", encoding="utf-8", newline="\n")
    try:
        handle.write(text + "\n")
    finally:
        handle.close()
    return path


def main():
    check(LINE)
    path = emit(LINE)
    # Read back what was written: a partial or mangled write must fail
    # loudly here instead of shipping a broken entry to the judge.
    handle = open(path, encoding="utf-8")
    try:
        saved = handle.read()
    finally:
        handle.close()
    if saved != LINE + "\n":
        print("entry.txt does not match the validated line", file=sys.stderr)
        raise SystemExit(1)
    print("wrote %d characters to %s" % (len(LINE), path))


if __name__ == "__main__":
    main()
