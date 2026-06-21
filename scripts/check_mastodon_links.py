from __future__ import annotations

import argparse
import sys
from pathlib import Path

from mastodon import MastodonError

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import mastodon, youtuber_store


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify every source Mastodon account through its server API.")
    parser.add_argument("--timeout", type=float, default=12.0)
    args = parser.parse_args()

    try:
        youtubers = youtuber_store.load()
    except (OSError, ValueError) as exc:
        print(exc)
        return 1

    failures: list[str] = []
    for creator in youtubers:
        url = creator["mastodon_url"]
        try:
            profile = mastodon.lookup_profile(url, timeout=args.timeout)
            print(f"OK {creator['name']}: @{profile.acct}")
        except (ValueError, MastodonError) as exc:
            failures.append(f"{creator['name']}: {url} -> {exc}")

    if failures:
        print("\nInvalid Mastodon profiles:")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print(f"\nVerified {len(youtubers)} Mastodon profiles.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
