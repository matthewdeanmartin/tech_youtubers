from __future__ import annotations

import argparse
import json
import re
import sqlite3
import unicodedata
from pathlib import Path

from pipeline import categorize, mastodon_discovery, youtuber_store

CATEGORY_OVERRIDES_PATH = Path(__file__).parent.parent / "data" / "category_overrides.json"


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii").casefold()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_value).strip("-")
    return slug or "creator"


def clean_name(value: str, acct: str) -> str:
    name = re.sub(r":\w+:", "", value or "")
    name = " ".join(name.split()).strip()
    return name or acct.split("@", 1)[0]


def description(account: dict) -> str:
    text = categorize.plain_text(str(account.get("note") or ""))
    text = re.sub(r"\s+", " ", text).strip()
    return text[:300] + ("…" if len(text) > 300 else "")


def profile_url(account: dict) -> str:
    return str(account.get("url") or "")


def choose_youtube(rows: list[sqlite3.Row]) -> sqlite3.Row:
    return sorted(
        rows,
        key=lambda row: (
            not row["youtube_url"].split("/")[-1].startswith("@"),
            len(row["youtube_url"]),
        ),
    )[0]


def build_catalog(db: sqlite3.Connection) -> list[dict]:
    categorize.classify_database(db)
    overrides = (
        json.loads(CATEGORY_OVERRIDES_PATH.read_text(encoding="utf-8"))
        if CATEGORY_OVERRIDES_PATH.exists()
        else {}
    )
    rows = db.execute(
        """
        SELECT p.*, y.youtube_url, y.evidence_source, c.category, c.confidence,
               c.matched_terms_json, c.account_type
        FROM profiles p
        JOIN youtube_links y USING (acct)
        JOIN classifications c USING (acct)
        ORDER BY p.acct COLLATE NOCASE, y.youtube_url
        """
    ).fetchall()
    grouped: dict[str, list[sqlite3.Row]] = {}
    for row in rows:
        grouped.setdefault(row["acct"], []).append(row)

    existing_by_mastodon = {
        item["mastodon_url"].casefold(): item
        for item in youtuber_store.load()
    }
    used_ids: set[str] = set()
    catalog: list[dict] = []
    for acct, account_rows in grouped.items():
        row = choose_youtube(account_rows)
        account = json.loads(row["raw_json"])
        override = overrides.get(acct, {})
        category = override.get("category", row["category"])
        if category not in categorize.CATEGORY_LABELS:
            raise ValueError(f"{acct}: unknown category override {category!r}")
        mastodon_url = profile_url(account)
        old = existing_by_mastodon.get(mastodon_url.casefold(), {})
        name = clean_name(str(account.get("display_name") or ""), acct)
        base_id = old.get("id") or slugify(name)
        creator_id = base_id
        suffix = 2
        while creator_id in used_ids:
            creator_id = f"{base_id}-{suffix}"
            suffix += 1
        used_ids.add(creator_id)
        catalog.append(
            {
                "id": creator_id,
                "name": old.get("name") or name,
                "category": category,
                "category_confidence": "curated" if override else row["confidence"],
                "category_evidence": (
                    [override["reason"]]
                    if override.get("reason")
                    else json.loads(row["matched_terms_json"])
                ),
                "account_type": row["account_type"],
                "youtube_url": row["youtube_url"],
                "youtube_evidence_source": row["evidence_source"],
                "mastodon_url": mastodon_url,
                "mastodon_acct": acct,
                "description": old.get("description") or description(account),
                "followers": row["followers_count"],
                "reviewed": old.get("reviewed", False),
                "review_slug": old.get("review_slug", creator_id),
            }
        )
    return sorted(
        catalog,
        key=lambda item: (
            categorize.CATEGORY_SORTORDER.index(item["category"]),
            item["account_type"] != "native",
            item["name"].casefold(),
        ),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish categorized YouTube-linked Mastodon profiles.")
    parser.add_argument("--db", type=Path, default=mastodon_discovery.DEFAULT_DB_PATH)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    db = mastodon_discovery.connect(args.db)
    catalog = build_catalog(db)
    if args.dry_run:
        counts: dict[tuple[str, str], int] = {}
        for item in catalog:
            key = (item["category"], item["account_type"])
            counts[key] = counts.get(key, 0) + 1
        print(json.dumps({f"{k[0]}:{k[1]}": v for k, v in counts.items()}, indent=2))
    else:
        youtuber_store.save(catalog)
        print(f"Published {len(catalog)} categorized profiles to {youtuber_store.YOUTUBERS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
