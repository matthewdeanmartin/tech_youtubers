Title: Bulk Follow Guide
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

```

---

### Mastodon Bulk Follow

Mastodon allows you to import CSV files containing lists of people to follow.

#### Step 1: Copy CSV Content
Copy the CSV content below and save it as `follows.csv` on your computer:

```csv
Account address,Show boosts
@fireship@mastodon.social,true
@craftzdog@mastodon.social,true
@coreyschafer@mastodon.social,true
@geerlingguy@mastodon.social,true
@thelinuxEXP@mastodon.social,true
@mattferrell@mastodon.social,true
@zollotech@mastodon.social,true
@tomlawrence@infosec.exchange,true
@BrodieOnLinux@mstdn.social,true
@technotim@mastodon.social,true
@notthebee@tilde.zone,true
@EposVox@glitch.lgbt,true
@davidbombal@infosec.exchange,true
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
