from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) in sys.path:
    sys.path.remove(str(SCRIPT_DIR))
sys.path.insert(0, str(REPO_ROOT))

from mastodon import MastodonAPIError, MastodonError
from pipeline import categorize, mastodon, mastodon_discovery, youtuber_store

DEFAULT_QUERIES = [
    "youtube",
    "youtuber",
    "video creator youtube",
    "gaming youtube",
    "vtuber youtube",
    "music youtube",
    "art youtube",
    "science youtube",
    "education youtube",
    "history youtube",
    "news youtube",
    "politics youtube",
    "film youtube",
    "travel youtube",
    "photography youtube",
    "cooking youtube",
    "programming youtube",
    "linux youtube",
    "cybersecurity youtube",
    "hardware youtube",
    # Twitch streamers and PeerTube (the Fediverse video platform) creators are
    # now first-class evidence alongside YouTube.
    "twitch",
    "twitch streamer",
    "gaming twitch",
    "live streamer",
    "peertube",
    "peertube creator",
    "video creator fediverse",
]


def collect(args: argparse.Namespace) -> int:
    api = mastodon.client_from_env()
    source_instance = mastodon.parse_profile_url(
        f"{api.api_base_url}/@placeholder"
    )[0]
    db = mastodon_discovery.connect(args.db)
    queries = args.query or DEFAULT_QUERIES
    stored = youtube_profiles = 0

    for query in queries:
        for page in range(args.pages):
            offset = page * args.limit
            try:
                accounts = list(
                    api.account_search(
                        query,
                        limit=args.limit,
                        offset=offset,
                        resolve=False,
                    )
                )
            except (MastodonAPIError, MastodonError) as exc:
                print(f"WARN search {query!r} offset {offset}: {exc}", file=sys.stderr)
                break
            if not accounts:
                break
            for account in accounts:
                _, link_count = mastodon_discovery.store_account(
                    db,
                    account,
                    source_instance=source_instance,
                    query=query,
                    result_offset=offset,
                )
                stored += 1
                youtube_profiles += bool(link_count)
            db.commit()
            print(f"{query!r} offset={offset}: {len(accounts)} profiles")
            if len(accounts) < args.limit:
                break

    totals = mastodon_discovery.stats(db)
    print(
        f"Stored {stored} search results ({youtube_profiles} with channel links this run). "
        f"Database: {totals['profiles']} unique profiles, "
        f"{totals['profiles_with_youtube']} with YouTube channel evidence."
    )
    return 0


def seed(args: argparse.Namespace) -> int:
    api = mastodon.client_from_env()
    db = mastodon_discovery.connect(args.db)
    creators = youtuber_store.load()
    failures = 0
    for creator in creators:
        try:
            account = mastodon.lookup_account(api, creator["mastodon_url"])
            acct, links = mastodon_discovery.store_account(
                db, account, source_instance="seed", query="existing-directory"
            )
            print(f"{creator['name']}: @{acct} ({links} YouTube channel link(s))")
        except (MastodonError, ValueError) as exc:
            failures += 1
            print(f"WARN {creator['name']}: {exc}", file=sys.stderr)
    db.commit()
    print(f"Seeded {len(creators) - failures}/{len(creators)} existing creators.")
    return 1 if failures else 0


def audit(args: argparse.Namespace) -> int:
    api = mastodon.client_from_env()
    db = mastodon_discovery.connect(args.db)
    creators = youtuber_store.load()
    kept: list[dict] = []
    removed: list[tuple[dict, str]] = []

    for creator in creators:
        try:
            account = mastodon.lookup_account(api, creator["mastodon_url"])
            mastodon_discovery.store_account(
                db, account, source_instance="audit", query="existing-directory"
            )
            links = mastodon_discovery.youtube_links(account)
            if not links:
                removed.append((creator, "Mastodon profile has no direct YouTube channel link"))
                continue
            kept.append(creator)
        except (MastodonError, ValueError) as exc:
            removed.append((creator, f"Mastodon lookup failed: {exc}"))

    db.commit()
    for creator, reason in removed:
        print(f"REMOVE {creator['name']}: {reason}")
    print(f"Keep {len(kept)}; remove {len(removed)}.")

    if args.write:
        youtuber_store.save(kept)
        print(f"Wrote {youtuber_store.YOUTUBERS_PATH}")
    elif removed:
        print("Dry run only; pass --write to replace the published dataset.")
    return 0


def report(args: argparse.Namespace) -> int:
    db = mastodon_discovery.connect(args.db)
    totals = mastodon_discovery.stats(db)
    print(json.dumps(totals, indent=2))
    for item in mastodon_discovery.candidates(db, args.limit):
        print(
            f"{item.followers_count:>9}  @{item.acct:<40}  "
            f"{item.youtube_url}  [{item.evidence_source}]"
        )
    return 0


def classify(args: argparse.Namespace) -> int:
    db = mastodon_discovery.connect(args.db)
    counts = categorize.classify_database(db)
    print(f"Classified {sum(counts.values())} profiles:")
    for category in categorize.CATEGORY_SORTORDER:
        print(f"  {categorize.CATEGORY_LABELS[category]}: {counts.get(category, 0)}")
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(
        description="Mastodon-first discovery of profiles that link to YouTube channels."
    )
    root.add_argument(
        "--db",
        type=Path,
        default=mastodon_discovery.DEFAULT_DB_PATH,
        help="SQLite candidate database (default: data/mastodon_candidates.sqlite)",
    )
    commands = root.add_subparsers(dest="command", required=True)

    collect_parser = commands.add_parser("collect", help="Search Mastodon and store profile candidates.")
    collect_parser.add_argument("--query", action="append", help="Search query; may be repeated.")
    collect_parser.add_argument("--pages", type=int, default=10, help="Pages per query.")
    collect_parser.add_argument("--limit", type=int, default=40, choices=range(1, 41))
    collect_parser.set_defaults(func=collect)

    seed_parser = commands.add_parser("seed", help="Fetch current directory profiles into SQLite.")
    seed_parser.set_defaults(func=seed)

    audit_parser = commands.add_parser(
        "audit", help="Keep only directory entries whose Mastodon profile links to YouTube."
    )
    audit_parser.add_argument("--write", action="store_true", help="Replace data/youtubers.json.")
    audit_parser.set_defaults(func=audit)

    report_parser = commands.add_parser("report", help="Show discovered profiles with YouTube evidence.")
    report_parser.add_argument("--limit", type=int, default=100)
    report_parser.set_defaults(func=report)

    classify_parser = commands.add_parser(
        "classify", help="Categorize every profile with YouTube channel evidence."
    )
    classify_parser.set_defaults(func=classify)
    return root


def main() -> int:
    args = parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
