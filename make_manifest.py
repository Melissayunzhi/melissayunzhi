"""Rescans images/ and rewrites images/manifest.js, which the work pages use to build their
"more photos" sections. Safe to run any time you add, rename or remove a photo -- unlike
build.py, this never touches works/*.html, so it won't overwrite anything you've written there.

Usage: python3 make_manifest.py .
"""
import sys
from build import build_photo_manifest

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    build_photo_manifest(root)
    print("wrote", root + "/images/manifest.js")
