"""Generate the public directory pages from data/youtubers.json."""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).parent))
from pipeline import categorize, youtuber_store

CONTENT_DIR = Path(__file__).parent / "content"
PAGES_DIR = CONTENT_DIR / "pages"
ARTICLES_DIR = CONTENT_DIR / "articles"
FOLLOW_TOOL_PATH = Path(__file__).parent / "static" / "mastodon-follow" / "index.html"

PAGES_DIR.mkdir(parents=True, exist_ok=True)
ARTICLES_DIR.mkdir(parents=True, exist_ok=True)

CATEGORY_LABELS = categorize.CATEGORY_LABELS
CATEGORY_SORTORDER = categorize.CATEGORY_SORTORDER
ACCOUNT_TYPE_LABELS = {
    "native": "Mastodon",
    "rss-feed": "Automated feed",
    "channel-feed": "Automated feed",
    "bridge": "Bridge",
    "bot": "Bot",
}

# Account types that are unattended automation. They are collected on the
# dedicated bots page (grouped by topic) rather than cluttering the topic
# pages. Bridges are excluded because they are usually real people relayed
# via a fedibridge instance.
BOT_ACCOUNT_TYPES = {"rss-feed", "channel-feed", "bot"}


def _social_link(url: str | None) -> str:
    if not url:
        return "—"
    parsed = urlparse(url)
    username = parsed.path.strip("/").removeprefix("@")
    handle = f"@{username}@{parsed.netloc}"
    return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{html.escape(handle)}</a>'


def _mastodon_account(url: str) -> str:
    parsed = urlparse(url)
    username = parsed.path.strip("/").removeprefix("@")
    return f"{username}@{parsed.netloc}"


def sync_follow_tool(youtubers: list[dict]) -> None:
    text = FOLLOW_TOOL_PATH.read_text(encoding="utf-8")
    rows = []
    for creator in youtubers:
        if creator.get("account_type") != "native":
            continue
        row = {
            "name": creator["name"],
            "acct": _mastodon_account(creator["mastodon_url"]),
            "niche": creator.get("description") or "",
        }
        rows.append(f"    {json.dumps(row, ensure_ascii=False)},")
    replacement = "/* DATA:START */\n  const STARTER_ACCOUNTS = [\n" + "\n".join(rows) + "\n  ];\n  /* DATA:END */"
    updated, count = re.subn(
        r"/\* DATA:START \*/.*?/\* DATA:END \*/",
        replacement,
        text,
        flags=re.DOTALL,
    )
    if count != 1:
        raise ValueError(f"{FOLLOW_TOOL_PATH}: expected exactly one generated data block")
    FOLLOW_TOOL_PATH.write_text(updated, encoding="utf-8")


def sync_reviews(youtubers: list[dict]) -> tuple[list[dict], int]:
    updated = 0
    for creator in youtubers:
        slug = creator.get("review_slug") or creator.get("id")
        if (ARTICLES_DIR / f"{slug}.md").exists() and not creator.get("reviewed"):
            creator["reviewed"] = True
            creator["review_slug"] = slug
            updated += 1
    return youtubers, updated


def generate_youtubers_page(youtubers: list[dict]) -> str:
    def category_sort(item: dict) -> int:
        try:
            return CATEGORY_SORTORDER.index(item.get("category", "other"))
        except ValueError:
            return 99

    sorted_creators = sorted(
        youtubers,
        key=lambda item: (
            item.get("account_type") != "native",
            category_sort(item),
            item.get("name", "").casefold(),
        ),
    )
    rows = []
    for creator in sorted_creators:
        name = html.escape(creator.get("name", ""))
        youtube = html.escape(creator.get("primary_url") or creator.get("youtube_url", ""), quote=True)
        category = CATEGORY_LABELS.get(creator.get("category", "other"), "Other")
        account_type = ACCOUNT_TYPE_LABELS.get(creator.get("account_type", "native"), "Other")
        followers = str(creator.get("followers") or "—")
        lang = html.escape(creator.get("language") or "en", quote=True)
        rows.append(
            f'        <tr data-lang="{lang}">'
            f'<td class="tools-table__name"><a href="{youtube}" target="_blank" rel="noopener noreferrer">{name}</a></td>'
            f"<td>{html.escape(category)}</td>"
            f"<td>{html.escape(account_type)}</td>"
            f"<td>{html.escape(followers)}</td>"
            f"<td>{_social_link(creator.get('mastodon_url'))}</td>"
            "</tr>"
        )

    filter_bar = (
        '<div class="lang-filter-bar">'
        '<p>Showing creators in your browser language.</p>'
        '<button id="lang-filter-btn" type="button" aria-pressed="false">'  # label set by JS
        "&#x1F30D; Show all languages"
        "</button>"
        "</div>"
        '<p id="lang-filter-empty" hidden>'
        "No creators match your browser language. "
        "Use the button above to show all languages."
        "</p>"
    )

    table = "\n".join(
        [
            filter_bar,
            '<table class="tools-table">',
            "    <thead>",
            "        <tr>",
            "            <th>YouTuber</th>",
            "            <th>Category</th>",
            "            <th>Account</th>",
            "            <th>Mastodon followers</th>",
            "            <th>Mastodon</th>",
            "        </tr>",
            "    </thead>",
            "    <tbody>",
            *rows,
            "    </tbody>",
            "</table>",
        ]
    )
    native_count = sum(item.get("account_type") == "native" for item in youtubers)
    feed_count = len(youtubers) - native_count
    return f"""Title: All YouTubers
Date: 2026-06-20
Slug: youtubers
sortorder: 2
Summary: YouTube creators and channel feeds discoverable on Mastodon.

## YouTubers on Mastodon

{len(youtubers)} evidence-backed profiles: **{native_count} native Mastodon accounts** and
**{feed_count} automated feeds or bridges**. Native accounts are listed first because those are
the profiles where interaction is most likely.

{table}

Want to follow the native accounts in bulk? Head to the [Bulk Follow Page]({{filename}}bulk-follow.md).

## Inclusion rule

- The Mastodon profile must contain a direct link to a YouTube channel.
- Automated channel feeds and bridges are labeled separately from native Mastodon accounts.
"""


def _lang_attr(creator: dict) -> str:
    """Return a data-lang HTML attribute string for the creator."""
    lang = html.escape(creator.get("language") or "en", quote=True)
    return f' data-lang="{lang}"'


def _creator_li(creator: dict, mastodon_label: str) -> str:
    """Render one directory entry as a self-contained HTML list item.

    We emit real HTML rather than Markdown because these `<li>` elements live
    inside a raw `<ul>` block; Pelican's Markdown processor does not descend
    into block-level raw HTML, so `**[name](url)**` would render literally.
    """
    lang = html.escape(creator.get("language") or "en", quote=True)
    name = html.escape(creator["name"])
    primary_url = html.escape(creator.get("primary_url") or creator["youtube_url"], quote=True)
    mastodon_url = html.escape(creator["mastodon_url"], quote=True)
    description = html.escape(creator.get("description") or "")
    return (
        f'<li data-lang="{lang}">'
        f'<strong><a href="{primary_url}" target="_blank" rel="noopener noreferrer">{name}</a></strong>'
        f' · <a href="{mastodon_url}" target="_blank" rel="noopener noreferrer">{mastodon_label}</a>'
        f" — {description}"
        "</li>"
    )


def _section(section_key: str, heading: str, list_items: list[str]) -> str:
    """Wrap a heading and list items in a data-lang-section div.

    Everything is real HTML — including the ``<h2>`` — because Markdown
    syntax inside a block-level raw HTML element is not processed by Pelican.
    """
    return (
        f'<div data-lang-section="{html.escape(section_key, quote=True)}">\n'
        f"<h2>{html.escape(heading)}</h2>\n\n"
        "<ul>\n" + "\n".join(list_items) + "\n</ul>\n"
        "</div>"
    )


def generate_category_page(category: str, youtubers: list[dict]) -> str:
    label = CATEGORY_LABELS[category]
    items = [item for item in youtubers if item.get("category") == category]
    # Bot/feed accounts are surfaced on their own page (see generate_bots_page),
    # so topic pages only carry native accounts and human-operated bridges.
    items = [item for item in items if item.get("account_type") not in BOT_ACCOUNT_TYPES]
    native = [item for item in items if item.get("account_type") == "native"]
    feeds = [item for item in items if item.get("account_type") != "native"]

    # Native section — wrapped in a data-lang-section div so JS can collapse
    # the whole block when all items are filtered out.
    native_items = [
        _creator_li(creator, "Mastodon")
        for creator in sorted(native, key=lambda item: item.get("name", "").casefold())
    ]

    if native_items:
        native_block = _section("native", f"Native Mastodon accounts ({len(native)})", native_items)
    else:
        native_block = (
            f"<h2>Native Mastodon accounts ({len(native)})</h2>\n\nNo native accounts in this category yet."
        )

    feeds_block = ""
    if feeds:
        feed_items = [
            _creator_li(creator, "Bridge")
            for creator in sorted(feeds, key=lambda item: item.get("name", "").casefold())
        ]
        feeds_block = "\n" + _section("feeds", f"Bridged accounts ({len(feeds)})", feed_items)

    return f"""Title: {label} YouTubers
Date: 2026-06-20
Slug: {category}
sortorder: {CATEGORY_SORTORDER.index(category) + 10}
Summary: {label} YouTube creators and channel feeds on Mastodon.

{native_block}{feeds_block}
"""


def generate_bots_page(youtubers: list[dict]) -> str:
    """Collect every automated feed/bot account on one page, grouped by topic."""
    bots = [item for item in youtubers if item.get("account_type") in BOT_ACCOUNT_TYPES]

    sections = []
    for category in CATEGORY_SORTORDER:
        in_category = [item for item in bots if item.get("category") == category]
        if not in_category:
            continue
        label = CATEGORY_LABELS[category]
        bot_items = [
            _creator_li(creator, "Feed")
            for creator in sorted(in_category, key=lambda item: item.get("name", "").casefold())
        ]
        sections.append(_section(f"bots-{category}", f"{label} ({len(in_category)})", bot_items))

    body = "\n\n".join(sections) if sections else "No automated feeds in the directory yet."

    return f"""Title: Automated Feeds & Bots
Date: 2026-06-20
Slug: bots
sortorder: 8
Summary: Automated channel feeds and bot accounts that relay YouTube content to Mastodon.

## Automated Feeds & Bots

These {len(bots)} accounts are unattended automation — RSS feeds and bots that mirror a
channel's uploads to the Fediverse. They are grouped here, by topic, so the topic pages stay
focused on accounts you can actually interact with.

{body}
"""


def generate_bulk_follow_page(youtubers: list[dict]) -> str:
    handles = [
        f"@{_mastodon_account(item['mastodon_url'])}"
        for item in youtubers
        if item.get("account_type") == "native"
    ]
    csv_rows = ["Account address,Show boosts", *(f"{handle},true" for handle in handles)]
    return f"""Title: Bulk Follow Guide
Date: 2026-06-20
Slug: bulk-follow
sortorder: 3
Summary: How to bulk follow native YouTuber accounts on Mastodon.

## Bulk Follow on Mastodon

This list contains native Mastodon accounts only. Automated RSS feeds and bridges are excluded so
the follow pack stays focused on profiles where interaction is possible.

```text
{chr(10).join(handles)}
```

### Import a following list

Save the following as `follows.csv`, then import it from your Mastodon server's
**Preferences → Import and export → Import → Following list** screen.

```csv
{chr(10).join(csv_rows)}
```

### Interactive follow tool

Use the **[Follow on Mastodon](/mastodon-follow/)** page to browse and follow native accounts
one-by-one or all at once using PKCE OAuth.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Pelican pages from youtubers.json")
    parser.add_argument("--dry-run", action="store_true", help="Print output without writing files")
    args = parser.parse_args()
    youtubers = youtuber_store.load()
    print(f"Loaded {len(youtubers)} YouTubers")
    youtubers, synced = sync_reviews(youtubers)
    if synced and not args.dry_run:
        youtuber_store.save(youtubers)

    generated = {
        "youtubers.md": generate_youtubers_page(youtubers),
        "bots.md": generate_bots_page(youtubers),
        "bulk-follow.md": generate_bulk_follow_page(youtubers),
        **{
            f"{category}.md": generate_category_page(category, youtubers)
            for category in CATEGORY_SORTORDER
        },
    }
    for filename, content in generated.items():
        path = PAGES_DIR / filename
        if args.dry_run:
            print(f"\n--- {path} ---\n{content[:300]}...")
        else:
            path.write_text(content, encoding="utf-8")
            print(f"Wrote {path}")
    if not args.dry_run:
        sync_follow_tool(youtubers)
        print(f"Updated {FOLLOW_TOOL_PATH}")


if __name__ == "__main__":
    main()
