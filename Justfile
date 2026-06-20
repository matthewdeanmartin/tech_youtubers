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

# Copy hand-crafted static pages into output/ after Pelican runs.
# These pages aren't Pelican content (complex JS, etc.) but must ship with the site.
# Pelican's DELETE_OUTPUT_DIRECTORY would wipe them if they lived only in output/.
copy-static:
    uv run python -c "
import shutil, pathlib
src = pathlib.Path('static')
dst = pathlib.Path('output')
if src.is_dir():
    for f in src.rglob('*'):
        if f.is_file():
            rel = f.relative_to(src)
            target = dst / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, target)
            print(f'  copied: {rel}')
"

# Full build: generate pages then build HTML then copy static files
build: generate-pages html copy-static

# Remove generated output
clean:
    uv run python -c "import shutil, pathlib; shutil.rmtree('output', ignore_errors=True)"

# Serve with live reload (Ctrl-C to stop)
serve:
    uv run pelican --listen content -o output -s pelicanconf.py

# Serve and auto-regenerate on content changes
devserver:
    uv run pelican --listen --autoreload content -o output -s pelicanconf.py

# Generate production HTML (publishconf uses DELETE_OUTPUT_DIRECTORY=True)
publish: generate-pages
    uv run pelican content -o output -s publishconf.py
    just copy-static

# ── Quality gates ─────────────────────────────────────────────────────────────

# Python-only deterministic gates: generated artifact lint + internal links
quality-python: html copy-static
    uv run python scripts/check_pelican_artifacts.py --site-dir output
    uv run python scripts/check_links.py --site-dir output --internal-only

# Cached external link audit
quality-links: html copy-static
    uv run python scripts/check_links.py --site-dir output

# Node-only gates: HTML validation, CSS browser support, accessibility
quality-node: html copy-static
    npm run quality

# Full quality pass
quality: build quality-python quality-node

