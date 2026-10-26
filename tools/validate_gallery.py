#!/usr/bin/env python3
"""USB_BSD: read-only static gallery manifest and media safety checks."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PHOTOS = DOCS / "assets" / "photos"
MANIFEST = DOCS / "data" / "gallery.json"
SOURCE_RE = re.compile(r"^assets/photos/[a-z0-9][a-z0-9_-]{0,70}\.(?:png|jpe?g|webp)$")
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SLOTS = {"desktop", "disk", "validation", "station", "other"}
LIMIT_BYTES = 5 * 1024 * 1024
errors: list[str] = []


def error(message: str) -> None:
    errors.append(message)
    print("FAIL:", message, file=sys.stderr)


def inspect_image(path: Path) -> None:
    raw = path.read_bytes()
    if len(raw) > LIMIT_BYTES:
        error(f"{path.name}: size exceeds 5 MiB")
        return
    ext = path.suffix.lower()

    if ext == ".png":
        if not raw.startswith(b"\x89PNG\r\n\x1a\n"):
            error(f"{path.name}: incorrect PNG signature")
            return
        index = 8
        while index + 12 <= len(raw):
            n = int.from_bytes(raw[index:index + 4], "big")
            kind = raw[index + 4:index + 8]
            if kind in {b"eXIf", b"tEXt", b"zTXt", b"iTXt"}:
                error(f"{path.name}: metadata chunk {kind.decode('ascii')} present")
            index += 12 + n
            if kind == b"IEND":
                break

    elif ext in {".jpg", ".jpeg"}:
        if not raw.startswith(b"\xff\xd8\xff"):
            error(f"{path.name}: incorrect JPEG signature")
            return
        for marker in (b"Exif\x00\x00", b"http://ns.adobe.com/xap/1.0/", b"Photoshop 3.0"):
            if marker in raw:
                error(f"{path.name}: EXIF/XMP/Photoshop metadata present")
                break

    elif ext == ".webp":
        if not (raw.startswith(b"RIFF") and raw[8:12] == b"WEBP"):
            error(f"{path.name}: incorrect WEBP signature")
            return
        index = 12
        while index + 8 <= len(raw):
            kind = raw[index:index + 4]
            n = int.from_bytes(raw[index + 4:index + 8], "little")
            if kind in {b"EXIF", b"XMP "}:
                error(f"{path.name}: metadata chunk present")
            index += 8 + n + (n % 2)


def validate() -> int:
    if not MANIFEST.is_file():
        error("Missing docs/data/gallery.json")
        return 1
    for dep in ["index.html", "assets/site.css", "assets/gallery.js"]:
        if not (DOCS / dep).is_file():
            error(f"Missing site dependency: {dep}")
    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        error(f"Invalid manifest: {exc}")
        return 1
    if not isinstance(data, dict) or data.get("schemaVersion") != 1:
        error("Manifest schemaVersion must be 1")
        return 1
    photos = data.get("photos")
    if not isinstance(photos, list) or len(photos) > 24:
        error("photos must be an array with at most 24 entries")
        return 1
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    for index, item in enumerate(photos):
        prefix = f"photos[{index}]"
        if not isinstance(item, dict):
            error(f"{prefix}: must be an object")
            continue
        photo_id = item.get("id")
        src = item.get("src")
        slot = item.get("slot")
        if not isinstance(photo_id, str) or not ID_RE.fullmatch(photo_id):
            error(f"{prefix}: invalid id")
        elif photo_id in seen_ids:
            error(f"{prefix}: duplicate id")
        else:
            seen_ids.add(photo_id)
        if slot not in SLOTS:
            error(f"{prefix}: invalid slot")
        for key, maximum in (("title", 90), ("alt", 200), ("caption", 360), ("category", 60)):
            value = item.get(key)
            if not isinstance(value, str) or not 3 <= len(value.strip()) <= maximum:
                error(f"{prefix}: invalid or missing {key}")
        if not isinstance(src, str) or not SOURCE_RE.fullmatch(src):
            error(f"{prefix}: invalid local image path")
            continue
        if src in seen_paths:
            error(f"{prefix}: duplicate image path")
        seen_paths.add(src)
        filename = DOCS / src
        if not filename.is_file() or filename.is_symlink():
            error(f"{prefix}: image missing or symlink: {src}")
        else:
            inspect_image(filename)
    if errors:
        print(f"FAIL: {len(errors)} gallery validation error(s)", file=sys.stderr)
        return 1
    print(f"PASS: static website assets and {len(photos)} verified manifest entries")
    print("NOTICE: visible image content requires separate human privacy review")
    return 0


if __name__ == "__main__":
    raise SystemExit(validate())
