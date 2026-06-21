"""Heuristic language detection for youtubers.json.

Detects whether a creator's content is primarily Japanese (CJK characters
in name or description) or English, and stamps the ``language`` field with a
BCP 47 base tag ("ja" / "en").

Run locally and commit the updated youtubers.json.  New entries with an
existing non-null language tag are left unchanged so manual overrides survive.

Usage:
    uv run python scripts/detect_language.py [--dry-run]
"""
from __future__ import annotations

import argparse
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import youtuber_store


# ---------------------------------------------------------------------------
# Heuristics
# ---------------------------------------------------------------------------

def _cjk_ratio(text: str) -> float:
    """Fraction of *letter* codepoints that are CJK / kana / hangul."""
    if not text:
        return 0.0
    letters = [c for c in text if unicodedata.category(c).startswith("L")]
    if not letters:
        return 0.0
    cjk = [
        c for c in letters
        if (
            "\u3000" <= c <= "\u9fff"   # CJK unified + kana blocks
            or "\uac00" <= c <= "\ud7ff"  # Hangul
            or "\uf900" <= c <= "\ufaff"  # CJK compatibility
            or "\u3400" <= c <= "\u4dbf"  # CJK extension A
        )
    ]
    return len(cjk) / len(letters)


def detect_language(creator: dict) -> str:
    """Return a BCP 47 base language tag for the creator."""
    name = creator.get("name") or ""
    description = creator.get("description") or ""

    # RSS-bot accounts on rss-mstdn.studiofreesia.com always append Japanese
    # boilerplate to the description; only trust the channel name for those.
    is_rss_bot = "rss-mstdn.studiofreesia.com" in (creator.get("mastodon_acct") or "")
    if is_rss_bot:
        text = name
    else:
        # Weight name heavily: repeat it 5 times so a Japanese name wins over
        # an incidental CJK character in an otherwise English description.
        text = (name + " ") * 5 + description

    if _cjk_ratio(text) > 0.15:
        return "ja"
    # Future heuristics (German, French, ...) can slot in here.
    return "en"



# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Stamp BCP 47 language tags onto youtubers.json")
    parser.add_argument("--dry-run", action="store_true", help="Print changes without writing")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Re-detect even when language is already set",
    )
    args = parser.parse_args()

    youtubers = youtuber_store.load()
    changed = 0
    for creator in youtubers:
        existing = creator.get("language")
        if existing and not args.overwrite:
            continue
        lang = detect_language(creator)
        if lang != existing:
            if args.dry_run:
                print(f"  {creator['id']}: {existing!r} -> {lang!r}")
            creator["language"] = lang
            changed += 1

    print(f"{'Would update' if args.dry_run else 'Updated'} {changed} entries.")
    if not args.dry_run and changed:
        youtuber_store.save(youtubers)
        print("Saved youtubers.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
