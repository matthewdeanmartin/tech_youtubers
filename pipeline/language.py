"""Heuristic language detection shared by the publish pipeline and the
stand-alone ``scripts/detect_language.py`` tool.

Detects whether a creator's content is primarily Japanese (CJK characters in
name or description) or English, and returns a BCP 47 base tag ("ja" / "en").
"""
from __future__ import annotations

import unicodedata


def cjk_ratio(text: str) -> float:
    """Fraction of *letter* codepoints that are CJK / kana / hangul."""
    if not text:
        return 0.0
    letters = [c for c in text if unicodedata.category(c).startswith("L")]
    if not letters:
        return 0.0
    cjk = [
        c
        for c in letters
        if (
            "　" <= c <= "鿿"  # CJK unified + kana blocks
            or "가" <= c <= "퟿"  # Hangul
            or "豈" <= c <= "﫿"  # CJK compatibility
            or "㐀" <= c <= "䶿"  # CJK extension A
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

    if cjk_ratio(text) > 0.15:
        return "ja"
    # Future heuristics (German, French, ...) can slot in here.
    return "en"
