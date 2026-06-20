# Tech YouTubers Directory

A static website listing and reviewing tech YouTubers with an active Mastodon or Bluesky presence, organized by their primary tech stack.

This website makes it easy for users new to Mastodon and Bluesky to find and follow the programming teachers, content creators, and tech celebs they know.

## Features

- **Organized by Tech Stack**: Easily browse creators focusing on JavaScript, Python, Rust, Go, Mobile, Databases, etc.
- **Bulk Follow lists**: Copy-paste handle lists or download a CSV to upload directly to Mastodon.
- **Creator Profiles**: Custom bio pages and reviews of their typical content and social accounts.
- **Comprehensive Quality Gates**: Built-in HTML validation, link checking, browser compatibility audit, and accessibility (WCAG2AA) verification.

## Architecture

This site is built with:
- **[Pelican](https://getpelican.com/)**: Python static site generator.
- **JSON Database**: `data/youtubers.json` stores creator metadata.
- **Vanilla CSS**: Premium dark/light themes without utility classes.

## Development Tasks

The project uses `just` (or `make`) for task running:

```bash
# Install and synchronize Python and Node dependencies
just sync
npm install

# Generate content files from data/youtubers.json
just generate-pages

# Generate stub profiles for unreviewed creators
just stubs

# Build the Pelican HTML site
just html

# Build the site and serve with auto-reload
just devserver

# Run all quality checks (HTML, CSS compatibility, Links, a11y)
just quality
```

## Contributing

Suggestions are welcome! To add a creator:
1. Ensure the creator has a YouTube channel and a Mastodon or Bluesky profile.
2. Add them to `data/youtubers.json`.
3. Run `just build` to generate the new pages.
