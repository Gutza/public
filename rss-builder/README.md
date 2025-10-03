rss-builder
===========

Minimal, no-dependency RSS 2.0 generator for this repository.

What it does
------------

- Scans markdown files in the repo (excluding `rss-builder/` and `images/`).
- Extracts:
  - Title: first `# H1` or filename without the date prefix
  - Date: from filename prefix `YYYY-MM-DD` or file mtime
  - Summary: first paragraph after the H1 (markdown links stripped)
- Writes `rss-feed.xml` at the repo root.

Installation
------------

This project uses `uv`. From the repo root:

```powershell
uv run python rss-builder/main.py --help
```

Usage
-----

```powershell
uv run python rss-builder/main.py `
  --base-url "https://gutza.github.io/public/" `
  --title "Public essays" `
  --description "Various public essays" `
   --feed-url "https://gutza.github.io/public/rss-feed.xml" `
  --limit 50 `
  --output rss-feed.xml `
  --verbose
```

Common flags
------------

- `--base-url`: Base site URL to prefix article paths. Ensure it corresponds to how your markdown files are published. A trailing slash is added if missing.
- `--limit`: Maximum number of items in the feed (newest first).
- `--output`: Target path for the generated XML (default: repo root `rss-feed.xml`).
- `--verbose`: Print processed items and final output path.
 - `--feed-url`: Canonical URL of this RSS feed; adds `<atom:link rel="self">`.

Notes
-----

- URL paths are derived from the markdown file path without the `.md` extension and URL-encoded. For example, `2025-10-01 Abortion Was Never The Issue.md` becomes `.../2025-10-01%20Abortion%20Was%20Never%20The%20Issue`.
- If a file lacks an H1, the filename (without the date prefix) is used for the title.
- The channel title/description defaults are derived from the root `README.md` when possible; otherwise simple fallbacks are used.
 - The feed declares the Atom namespace and includes a self-referencing `<atom:link rel="self" type="application/rss+xml">`.
