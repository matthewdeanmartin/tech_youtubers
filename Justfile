# Tech YouTubers Directory — task runner
# Run `just` to see available recipes.

set dotenv-load := true

# ── Dependency management ──────────────────────────────────────────────────────

# Install / sync Python dependencies
sync:
    uv sync

# ── Page generation ────────────────────────────────────────────────────────────

# Regenerate all Pelican content pages from data/youtubers.json
generate-pages:
    uv run python generate_pages.py

# Preview page generation without writing
generate-pages-dry-run:
    uv run python generate_pages.py --dry-run

# Generate stub articles for all unreviewed YouTubers
stubs:
    uv run python generate_review_stubs.py

# Overwrite all existing stubs (use with care — destroys hand-written prose)
stubs-force:
    uv run python generate_review_stubs.py --overwrite

# ── Site build ─────────────────────────────────────────────────────────────────

# Build the Pelican site
html:
    uv run pelican content -o output -s pelicanconf.py

# Full build: generate pages then build HTML
build: generate-pages html

# Remove generated output
clean:
    uv run python -c "import shutil, pathlib; shutil.rmtree('output', ignore_errors=True)"

# Serve with live reload (Ctrl-C to stop)
serve:
    uv run pelican --listen content -o output -s pelicanconf.py

# Serve and auto-regenerate on content changes
devserver:
    uv run pelican --listen --autoreload content -o output -s pelicanconf.py

# Generate production HTML
publish:
    uv run pelican content -o output -s publishconf.py

# ── Quality gates ─────────────────────────────────────────────────────────────

# Python-only deterministic gates: generated artifact lint + internal links
quality-python: html
    uv run python scripts/check_pelican_artifacts.py --site-dir output
    uv run python scripts/check_links.py --site-dir output --internal-only

# Cached external link audit
quality-links: html
    uv run python scripts/check_links.py --site-dir output

# Node-only gates: HTML validation, CSS browser support, accessibility
quality-node: html
    npm run quality

# Full quality pass
quality: build quality-python quality-node
