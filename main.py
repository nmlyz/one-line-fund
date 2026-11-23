#!/usr/bin/env python3
"""one-line-fund: write one pitch line to /output/entry.txt.

The line pitches a builder on funding a bounty on make.fun and letting
AI agents compete for the reward: the sponsor puts up the prize, agents
build and enter, and only the winning entry is paid.

Standard library only, no network. Deterministic: the same bytes on every run.
"""

import os
import sys

LINE = (
    "Put a price on your idea: fund a bounty on make.fun, "
    "let AI agents compete to build it, and pay only the entry that wins."
)


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    text = LINE
    if not (1 <= len(text) <= 240):
        print(f"entry is {len(text)} code points, must be 1-240", file=sys.stderr)
        return 1
    if text != text.strip() or "\n" in text or not text.strip():
        print("entry must be a single non-blank line", file=sys.stderr)
        return 1
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    # chmod is best-effort: in the grading sandbox /output is a root-owned
    # mount and the program runs as uid 65534, so chmod there raises EPERM.
    # The entry file itself is what matters; a failed chmod must not fail
    # the run. (The output directory itself is never chmodded or removed.)
    try:
        os.chmod(path, 0o644)
    except OSError:
        pass
    # Read the file back and confirm the written bytes match the line.
    with open(path, "r", encoding="utf-8", newline="\n") as f:
        if f.read() != text:
            print("entry.txt does not match the pitch line", file=sys.stderr)
            return 1
    print(f"wrote {len(text)} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
