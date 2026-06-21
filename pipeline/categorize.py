from __future__ import annotations

import html
import json
import re
import sqlite3
import unicodedata
from dataclasses import dataclass
from datetime import UTC, datetime
from html.parser import HTMLParser

CATEGORY_LABELS = {
    "technology": "Technology & Computing",
    "gaming": "Gaming & VTubers",
    "science-education": "Science & Education",
    "music": "Music",
    "art-making": "Art, Design & Making",
    "news-society": "News, Politics & Society",
    "culture-entertainment": "Culture & Entertainment",
    "lifestyle-hobbies": "Lifestyle, Travel & Hobbies",
    "other": "Other",
}

CATEGORY_SORTORDER = list(CATEGORY_LABELS)

TERMS = {
    "technology": {
        "linux": 5, "software": 5, "programming": 5, "coding": 5, "developer": 4,
        "cyber": 5, "infosec": 5, "security": 4, "technology": 4, "tech": 3,
        "computer": 4, "hardware": 5, "open source": 5, "opensource": 5,
        "self-host": 5, "homelab": 5, "server": 3, "cloud": 4, "devops": 5,
        "engineering": 3, "javascript": 5, "python": 5, "graphics programming": 6,
        "mobile": 2, "gadget": 3, "keyboard": 3, "pc": 2, "informatik": 4,
        "プログラミング": 5, "ソフトウェア": 5, "ゲーム制作": 3,
    },
    "gaming": {
        "gaming": 5, "gamer": 5, "gameplay": 5, "video game": 5, "speedrun": 6,
        "minecraft": 5, "geoguessr": 5, "vtuber": 6, "virtual youtuber": 6,
        "hololive": 6, "streamer": 3, "twitch": 2, "ゲーム": 5, "ゲーム実況": 6,
        "ゲーム配信": 6, "バーチャル": 4, "配信": 2, "実況": 3, "ポケモン": 5,
        "任天堂": 5, "playstation": 5, "capcom": 5, "カプコン": 5,
    },
    "science-education": {
        "science": 5, "physics": 5, "math": 5, "maths": 5, "research": 3,
        "teaching": 4, "teacher": 4, "education": 5, "educates": 4, "lecturer": 4,
        "tutorial": 3, "history": 4, "latin": 5, "classics": 4, "学習": 4,
        "研究": 3, "教育": 5,
    },
    "music": {
        "music": 5, "musician": 5, "concert": 5, "band": 4, "guitar": 4,
        "audio": 3, "radio": 3, "record label": 5, "dj": 4, "singing": 3,
        "singer": 4, "歌": 4, "音楽": 5, "ギター": 4, "dtmer": 4, "作曲": 4,
    },
    "art-making": {
        "artist": 5, "illustrator": 5, "illustration": 5, "drawing": 4,
        "design": 4, "designer": 4, "photography": 5, "photographer": 5,
        "maker": 4, "tinkerer": 3, "3d": 3, "animation": 4, "anime": 3,
        "art": 3, "craft": 4, "絵": 4, "イラスト": 5, "写真": 5, "漫画": 4,
        "アニメ": 4, "動画編集": 3,
    },
    "news-society": {
        "news": 6, "journalism": 5, "journalist": 5, "politics": 5,
        "political": 5, "political party": 5, "digital rights": 4,
        "human rights": 4, "society": 3, "law": 4,
        "reuters": 6, "bbc news": 6, "nhk": 5, "ニュース": 6, "新聞": 6,
        "共産党": 6, "民主党": 6, "弁護士": 5, "報道": 6,
    },
    "culture-entertainment": {
        "podcast": 5, "film": 4, "movie": 4, "television": 4, "tv": 3,
        "media": 3, "comedy": 4, "writer": 3, "author": 3, "story": 3,
        "entertainment": 5, "映画": 5, "小説": 4, "朗読": 4, "特撮": 5,
    },
    "lifestyle-hobbies": {
        "travel": 5, "outdoors": 5, "cycling": 4, "food": 4, "cooking": 4,
        "beauty": 4, "fitness": 4, "horse": 4, "equestrian": 5, "camera": 3,
        "asmr": 3, "散歩": 4, "旅行": 5, "競馬": 5, "卓球": 5, "カメラ": 3,
    },
}


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def plain_text(value: str) -> str:
    parser = TextExtractor()
    parser.feed(value or "")
    return " ".join(html.unescape(" ".join(parser.parts)).split())


def classification_text(account: dict) -> str:
    fields = account.get("fields") or []
    pieces = [
        str(account.get("display_name") or ""),
        plain_text(str(account.get("note") or "")),
    ]
    for field in fields:
        pieces.extend([plain_text(str(field.get("name") or "")), plain_text(str(field.get("value") or ""))])
    return unicodedata.normalize("NFKC", " ".join(pieces)).casefold()


def account_type(account: dict) -> str:
    acct = str(account.get("acct") or "").casefold()
    text = classification_text(account)
    if "rss-mstdn.studiofreesia.com" in acct or "rssフィードの内容を投稿するbot" in text:
        return "rss-feed"
    if "feedsin.space" in acct:
        return "channel-feed"
    if "brid.gy" in acct or "bridged from" in text:
        return "bridge"
    if account.get("bot"):
        return "bot"
    return "native"


@dataclass(frozen=True)
class Classification:
    category: str
    confidence: str
    matched_terms: tuple[str, ...]
    account_type: str


def classify(account: dict) -> Classification:
    text = classification_text(account)
    scores: dict[str, int] = {}
    matches: dict[str, list[str]] = {}
    for category, weighted_terms in TERMS.items():
        for term, weight in weighted_terms.items():
            if term in text:
                scores[category] = scores.get(category, 0) + weight
                matches.setdefault(category, []).append(term)

    if not scores:
        return Classification("other", "low", (), account_type(account))

    ranked = sorted(scores.items(), key=lambda item: (-item[1], CATEGORY_SORTORDER.index(item[0])))
    category, score = ranked[0]
    runner_up = ranked[1][1] if len(ranked) > 1 else 0
    margin = score - runner_up
    confidence = "high" if score >= 8 and margin >= 3 else "medium" if score >= 4 else "low"
    return Classification(category, confidence, tuple(matches.get(category, ())), account_type(account))


def classify_database(db: sqlite3.Connection) -> dict[str, int]:
    rows = db.execute(
        "SELECT acct, raw_json FROM profiles WHERE acct IN (SELECT DISTINCT acct FROM youtube_links)"
    ).fetchall()
    now = datetime.now(UTC).isoformat()
    counts: dict[str, int] = {}
    for row in rows:
        account = json.loads(row["raw_json"])
        result = classify(account)
        db.execute(
            """
            INSERT INTO classifications (
                acct, category, confidence, matched_terms_json, account_type, classified_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(acct) DO UPDATE SET
                category=excluded.category,
                confidence=excluded.confidence,
                matched_terms_json=excluded.matched_terms_json,
                account_type=excluded.account_type,
                classified_at=excluded.classified_at
            """,
            (
                row["acct"],
                result.category,
                result.confidence,
                json.dumps(result.matched_terms, ensure_ascii=False),
                result.account_type,
                now,
            ),
        )
        counts[result.category] = counts.get(result.category, 0) + 1
    db.commit()
    return counts
