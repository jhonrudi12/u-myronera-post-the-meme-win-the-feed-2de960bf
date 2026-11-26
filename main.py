#!/usr/bin/env python3
"""Entry program (Python, standard library only).

Same job as main.ts, the entrypoint the grader runs: copy POST.json from
the repository root to /output/POST.json, where the gate reads it. That is
all the program has to do. The entry is the post itself: the meme image
(meme.png, drawn in this session by draw_meme.py) is posted natively on X
from a public account with the text the rules ask for, POST.json names the
post, and the house reads the post's counts from X.

Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
stand in for /bot and /output:
  mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
import sys

BOT_DIR = os.environ.get("MAKEFUN_BOT_DIR", "/bot")
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUTPUT_DIR, exist_ok=True)
try:
    shutil.copyfile(os.path.join(BOT_DIR, "POST.json"),
                    os.path.join(OUTPUT_DIR, "POST.json"))
except OSError as err:
    print(f"POST.json could not be copied from {BOT_DIR}: {err}", file=sys.stderr)
    sys.exit(1)
