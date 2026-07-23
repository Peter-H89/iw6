#!/usr/bin/env python3
"""Regenerate the CMU Bright latin-subset woff2 files in this directory.

Usage:
    pip install fonttools brotli   (or use a throwaway venv)
    python3 subset.py              (run from this directory)

Sources are the TTFs from the `computer-modern` npm package (SIL OFL),
pinned by version below. The subset is Google Fonts' "latin" range: it
covers Dutch and French entirely (including oe-ligature and euro); math
glyphs are deliberately dropped because MathJax ships its own fonts.

The woff2 files are referenced by theme/vep.scss; keep the face list here
in sync with the @font-face rules there.
"""
import tempfile
import urllib.request
from pathlib import Path

from fontTools.subset import main as subset

VERSION = "0.1.2"
BASE = f"https://cdn.jsdelivr.net/npm/computer-modern@{VERSION}/fonts"
FACES = [
    "cmu-bright-500-roman",   # weight 400
    "cmu-bright-500-italic",  # weight 400 italic
    "cmu-bright-600-roman",   # weight 600
    "cmu-bright-700-roman",   # weight 700
    "cmu-bright-700-italic",  # weight 700 italic
]
LATIN = (
    "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,"
    "U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,"
    "U+FEFF,U+FFFD"
)

here = Path(__file__).parent
with tempfile.TemporaryDirectory() as tmp:
    for face in FACES:
        src = Path(tmp) / f"{face}.ttf"
        urllib.request.urlretrieve(f"{BASE}/{face}.ttf", src)
        out = here / f"{face}-latin.woff2"
        subset([
            str(src),
            f"--unicodes={LATIN}",
            "--layout-features=*",
            "--flavor=woff2",
            f"--output-file={out}",
        ])
        print(f"{out.name}: {out.stat().st_size // 1024} KB")
