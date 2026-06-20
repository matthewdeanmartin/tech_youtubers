"""
Generate Pelican content pages from data/youtubers.json.

Rewrites:
  - content/pages/youtubers.md          — full table sorted by tech stack
  - content/pages/{tech_stack}.md       — per tech stack pages
  - content/pages/bulk-follow.md        — bulk follow handle lists for import

Also syncs reviewed/review_slug in youtubers.json from existing article frontmatter.
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from pipeline import youtuber_store

CONTENT_DIR = Path(__file__).parent / "content"
PAGES_DIR = CONTENT_DIR / "pages"
ARTICLES_DIR = CONTENT_DIR / "articles"

# Create directories if they don't exist
PAGES_DIR.mkdir(parents=True, exist_ok=True)
ARTICLES_DIR.mkdir(parents=True, exist_ok=True)

TECH_STACK_LABELS = {
    "javascript": "JavaScript / TypeScript",
    "rust": "Rust",
    "go": "Go",
    "python": "Python",
    "mobile": "Mobile Development",
    "databases": "Databases & Systems",
    "devops": "DevOps & Cloud",
    "general": "General Tech",
}

TECH_STACK_SORTORDER = ["javascript", "rust", "go", "python", "mobile", "databases", "devops", "general"]


def _social_link(url: str | None, label: str) -> str:
    if not url:
        return "—"
    # Try to extract handle for display
    handle = url.split("/")[-1]
    if "@" not in handle and label.lower() == "mastodon":
        # Maybe handle looks like @username or username
        parts = [p for p in url.split("/") if p]
        if len(parts) >= 2:
            domain = parts[1]
            user = parts[2] if len(parts) > 2 else parts[1]
            if not user.startswith("@"):
                user = f"@{user}"
            handle = f"{user}@{domain}"
    elif label.lower() == "bluesky":
        # Usually it is handle.bsky.social
        pass
    return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{html.escape(handle)}</a>'


def _review_link(y: dict) -> str:
    if y.get("reviewed") and y.get("review_slug"):
        return f'<a href="../reviews/{y["review_slug"]}/">Bio &amp; Review</a>'
    return "—"


def sync_reviews(youtubers: list[dict]) -> tuple[list[dict], int]:
    """Read article frontmatter and update reviewed/review_slug in youtubers."""
    slug_map: dict[str, str] = {}
    for article in ARTICLES_DIR.glob("*.md"):
        text = article.read_text(encoding="utf-8")
        slug_match = re.search(r"^Slug:\s*(.+)$", text, re.MULTILINE)
        if slug_match:
            slug = slug_match.group(1).strip()
            slug_map[slug] = slug

    updated = 0
    for y in youtubers:
        slug = y.get("review_slug") or y.get("id")
        if (ARTICLES_DIR / f"{slug}.md").exists():
            if not y.get("reviewed"):
                y["reviewed"] = True
                y["review_slug"] = slug
                updated += 1
    return youtubers, updated


def generate_youtubers_page(youtubers: list[dict]) -> str:
    def stack_sort(t: dict) -> int:
        stack = t.get("tech_stack", "general")
        try:
            return TECH_STACK_SORTORDER.index(stack)
        except ValueError:
            return 99

    sorted_y = sorted(youtubers, key=lambda t: (stack_sort(t), t.get("name", "").lower()))

    rows = []
    for y in sorted_y:
        stack_label = TECH_STACK_LABELS.get(y.get("tech_stack", ""), y.get("tech_stack", ""))
        subs = y.get("subscribers") or "—"
        mastodon = _social_link(y.get("mastodon_url"), "Mastodon")
        bluesky = _social_link(y.get("bluesky_url"), "Bluesky")
        review = _review_link(y)
        name = y.get("name", "")
        yt_url = y.get("youtube_url")
        safe_name = html.escape(name)
        name_cell = f'<a href="{yt_url}" target="_blank" rel="noopener noreferrer">{safe_name}</a>' if yt_url else safe_name
        rows.append(
            "        <tr>"
            f'<td class="tools-table__name">{name_cell}</td>'
            f"<td>{html.escape(stack_label)}</td>"
            f"<td>{html.escape(subs)}</td>"
            f"<td>{mastodon}</td>"
            f"<td>{bluesky}</td>"
            f"<td>{review}</td>"
            "</tr>"
        )

    table = "\n".join([
        '<table class="tools-table">',
        "    <thead>",
        "        <tr>",
        "            <th>YouTuber</th>",
        "            <th>Tech Stack</th>",
        "            <th>Subscribers</th>",
        "            <th>Mastodon</th>",
        "            <th>Bluesky</th>",
        "            <th>Profile/Bio</th>",
        "        </tr>",
        "    </thead>",
        "    <tbody>",
        *rows,
        "    </tbody>",
        "</table>",
    ])

    reviewed_count = sum(1 for y in youtubers if y.get("reviewed"))

    return f"""Title: All Tech YouTubers
Date: 2026-06-20
Slug: youtubers
sortorder: 2
Summary: Full directory of tech YouTubers with social media presence.

## YouTube Directory

Organized by primary tech stack. {len(youtubers)} YouTubers listed &nbsp;·&nbsp; {reviewed_count} detailed bios.

{table}

Want to follow everyone in bulk? Head over to the [Bulk Follow Page]({{filename}}bulk-follow.md) to export follow lists!

## How to Suggest a YouTuber

Open a Pull Request on the repository or suggest via Mastodon/Bluesky. Criteria:
- Must produce regular tech/coding videos on YouTube.
- Must have a verifiable Mastodon or Bluesky profile.
"""


def generate_tech_stack_page(stack: str, youtubers: list[dict]) -> str:
    label = TECH_STACK_LABELS.get(stack, stack.capitalize())
    stack_y = [y for y in youtubers if y.get("tech_stack") == stack]
    if not stack_y:
        return ""

    reviewed = [y for y in stack_y if y.get("reviewed")]
    unreviewed = [y for y in stack_y if not y.get("reviewed")]

    sections = [f"## Detailed Profiles ({len(reviewed)})"]
    for y in sorted(reviewed, key=lambda t: t.get("name", "").lower()):
        slug = y.get("review_slug")
        name = y.get("name", "")
        desc = y.get("description") or ""
        link = f"[{name}](../reviews/{slug}/)" if slug else name
        sections.append(f"- **{link}** — {desc}")

    if unreviewed:
        sections.append(f"\n## Directory ({len(unreviewed)})")
        sections.append("Other tracked creators in this tech stack.")
        sections.append("")
        for y in sorted(unreviewed, key=lambda t: t.get("name", "").lower()):
            name = y.get("name", "")
            yt = y.get("youtube_url")
            desc = y.get("description") or ""
            link = f"[{name}]({yt})" if yt else name
            sections.append(f"- {link} — {desc}")

    body = "\n".join(sections)

    sortorder = TECH_STACK_SORTORDER.index(stack) + 10 if stack in TECH_STACK_SORTORDER else 50

    return f"""Title: {label} Creators
Date: 2026-06-20
Slug: {stack}
sortorder: {sortorder}
Summary: Tech YouTubers focusing on {label} who are on Mastodon or Bluesky.

{body}
"""


def generate_bulk_follow_page(youtubers: list[dict]) -> str:
    # Gather all non-null Mastodon links and Bluesky links
    mastodon_handles = []
    bluesky_handles = []

    for y in youtubers:
        m = y.get("mastodon_url")
        b = y.get("bluesky_url")
        if m:
            # e.g., https://mastodon.social/@fireship -> @fireship@mastodon.social
            parts = [p for p in m.split("/") if p]
            if len(parts) >= 2:
                domain = parts[1]
                user = parts[2] if len(parts) > 2 else parts[1]
                if not user.startswith("@"):
                    user = f"@{user}"
                mastodon_handles.append(f"{user}@{domain}")
        if b:
            # e.g., https://bsky.app/profile/fireship.dev -> fireship.dev
            parts = [p for p in b.split("/") if p]
            if len(parts) >= 2 and parts[1] == "profile":
                bluesky_handles.append(parts[2])

    m_list_str = "\n".join(mastodon_handles)
    b_list_str = "\n".join(bluesky_handles)

    # Let's generate a CSV for Mastodon import:
    # Mastodon follow import format: Account address,Show boosts (true/false)
    m_csv_rows = ["Account address,Show boosts"]
    for handle in mastodon_handles:
        m_csv_rows.append(f"{handle},true")
    m_csv_str = "\n".join(m_csv_rows)

    return f"""Title: Bulk Follow Guide
Date: 2026-06-20
Slug: bulk-follow
sortorder: 3
Summary: How to bulk follow all these tech YouTubers on Mastodon and Bluesky.

## Bulk Follow on Social Media

Instead of clicking follow one-by-one, you can use these lists to bulk follow creators on Mastodon or Bluesky.

---

### Bluesky Bulk Follow

On Bluesky, you can follow lists of users. Copy this list of handles to search and follow, or look out for a starter pack!

```text
{b_list_str}
```

---

### Mastodon Bulk Follow

Mastodon allows you to import CSV files containing lists of people to follow.

#### Step 1: Copy CSV Content
Copy the CSV content below and save it as `follows.csv` on your computer:

```csv
{m_csv_str}
```

#### Step 2: Import into Mastodon
1. Open your Mastodon Web UI.
2. Go to **Preferences** (or **Settings**).
3. Click on **Import and export** (or **Import**).
4. Under **Import**, select **Following list** as the import type.
5. Choose the `follows.csv` file you created and click **Upload**.

It may take a few minutes for your server to process all the accounts!

---

### Interactive Mastodon Follow Tool

Want a more interactive experience? Use the **[Follow on Mastodon](/mastodon-follow/)** page to:
- Browse all tech YouTubers with Mastodon accounts
- Authorize your instance using secure **PKCE OAuth** (no password or secret is ever stored)
- Follow creators one-by-one or all at once — like a Bluesky starter pack, but for Mastodon!
"""



def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Pelican pages from youtubers.json")
    parser.add_argument("--dry-run", action="store_true", help="Print output without writing files")
    args = parser.parse_args()

    youtubers = youtuber_store.load()
    print(f"Loaded {len(youtubers)} YouTubers")

    # Sync review status from existing articles
    youtubers, synced = sync_reviews(youtubers)
    if synced:
        print(f"Synced {synced} review entries from articles")
        if not args.dry_run:
            youtuber_store.save(youtubers)

    # Generate main directory page
    youtubers_content = generate_youtubers_page(youtubers)
    youtubers_path = PAGES_DIR / "youtubers.md"
    if args.dry_run:
        print(f"\n--- {youtubers_path} ---")
        print(youtubers_content[:500] + "...")
    else:
        youtubers_path.write_text(youtubers_content, encoding="utf-8")
        print(f"Wrote {youtubers_path}")

    # Generate bulk follow page
    bulk_content = generate_bulk_follow_page(youtubers)
    bulk_path = PAGES_DIR / "bulk-follow.md"
    if args.dry_run:
        print(f"\n--- {bulk_path} ---")
        print(bulk_content[:500] + "...")
    else:
        bulk_path.write_text(bulk_content, encoding="utf-8")
        print(f"Wrote {bulk_path}")

    # Generate per-tech-stack pages
    stacks = sorted({t.get("tech_stack", "general") for t in youtubers})
    for stack in stacks:
        content = generate_tech_stack_page(stack, youtubers)
        if not content:
            continue
        path = PAGES_DIR / f"{stack}.md"
        if args.dry_run:
            print(f"\n--- {path} (first 200 chars) ---")
            print(content[:200])
        else:
            path.write_text(content, encoding="utf-8")
            print(f"Wrote {path}")


if __name__ == "__main__":
    main()
