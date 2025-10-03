from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Optional, Tuple

import argparse
import datetime as dt
import re
import urllib.parse
from email.utils import format_datetime
from xml.sax.saxutils import escape as xml_escape


MAIN_FOLDER = Path(__file__).parent.parent
RSS_FEED_FILENAME = "rss-feed.xml"
RSS_FEED_PATH = MAIN_FOLDER / RSS_FEED_FILENAME
IGNORE_FILES = ["README.md"]
BASE_URL = "https://gutza.github.io/public/"

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="rss-builder",
        description=(
            "Scan markdown files and build an RSS 2.0 feed (no external deps)."
        ),
    )

    default_title = "Public essays"
    default_desc = _derive_default_description()
    default_base_url = BASE_URL

    parser.add_argument(
        "--base-url",
        dest="base_url",
        default=default_base_url,
        help="Base URL that article paths are appended to (e.g., https://example.com/blog/)",
    )
    parser.add_argument(
        "--title",
        default=default_title,
        help="Channel title for the RSS feed",
    )
    parser.add_argument(
        "--description",
        default=default_desc,
        help="Channel description for the RSS feed",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum number of items in the feed (newest first)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=RSS_FEED_PATH,
        help=f"Output file path (default: {RSS_FEED_PATH})",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print details while building the feed",
    )
    parser.add_argument(
        "--feed-url",
        default=f"{BASE_URL}{RSS_FEED_FILENAME}",
        help=(
            "Canonical URL of the generated feed (atom:link rel=\"self\"). "
            "Defaults to base-url + output filename."
        ),
    )

    return parser.parse_args(argv)


def _derive_default_description() -> str:
    readme_path = MAIN_FOLDER / "README.md"
    if not readme_path.exists():
        return "Feed of essays"
    try:
        first_line = readme_path.read_text(encoding="utf-8").splitlines()[0].strip()
        return first_line or "Feed of essays"
    except Exception:
        return "Feed of essays"


def find_markdown_files() -> List[Path]:
    all_md_files = list(MAIN_FOLDER.glob("*.md"))
    results: List[Path] = []
    for path in all_md_files:
        # Exclude files inside rss-builder or images by default
        if path.name in IGNORE_FILES:
            continue
        results.append(path)
    return results


def parse_article(path: Path) -> Optional[dict]:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None

    title = _extract_title(text)
    if not title:
        # Fall back to filename without date prefix if no H1
        title = _title_from_filename(path.name)

    published_at = _extract_date_from_filename(path.name) or _fallback_date_from_stat(path)
    summary = _extract_summary(text)
    rel_url_path = _relative_url_path(path)

    return {
        "title": title,
        "published_at": published_at,
        "summary": summary,
        "rel_url_path": rel_url_path,
        "source_path": path,
    }


def _extract_title(text: str) -> Optional[str]:
    for line in text.splitlines():
        m = re.match(r"^\s*#\s+(.+?)\s*$", line)
        if m:
            return m.group(1).strip()
    return None


def _title_from_filename(filename: str) -> str:
    m = re.match(r"^(\d{4}-\d{2}-\d{2})\s+(.+?)\.md$", filename)
    if m:
        return m.group(2)
    return Path(filename).stem


def _extract_date_from_filename(filename: str) -> Optional[dt.datetime]:
    m = re.match(r"^(\d{4}-\d{2}-\d{2})\s+.+?\.md$", filename)
    if not m:
        return None
    try:
        date = dt.datetime.strptime(m.group(1), "%Y-%m-%d").replace(tzinfo=dt.timezone.utc)
        return date
    except ValueError:
        return None


def _fallback_date_from_stat(path: Path) -> dt.datetime:
    ts = path.stat().st_mtime
    return dt.datetime.fromtimestamp(ts, tz=dt.timezone.utc)


def _extract_summary(text: str) -> str:
    lines = text.splitlines()
    # Skip until after the first H1
    idx = 0
    while idx < len(lines):
        if re.match(r"^\s*#\s+", lines[idx]):
            idx += 1
            break
        idx += 1
    # Skip blank lines
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    # Collect paragraph until blank line
    paragraph_lines: List[str] = []
    while idx < len(lines) and lines[idx].strip():
        paragraph_lines.append(lines[idx].strip())
        idx += 1
    paragraph = " ".join(paragraph_lines)
    # Strip basic markdown link syntax to keep readable text
    paragraph = re.sub(r"!\[[^\]]*\]\([^\)]*\)", "", paragraph)  # drop images
    paragraph = re.sub(r"\[([^\]]+)\]\([^\)]*\)", r"\1", paragraph)
    paragraph = re.sub(r"\s+", " ", paragraph).strip()
    return paragraph


def _relative_url_path(path: Path) -> str:
    # Make path relative to repo root
    rel_path = path.relative_to(MAIN_FOLDER)
    # Drop extension
    rel_no_ext = rel_path.with_suffix("")
    # Build URL path with URL-encoded segments
    encoded_segments = [urllib.parse.quote(part) for part in rel_no_ext.as_posix().split("/")]
    return "/".join(encoded_segments)


def build_rss(
    items: List[dict],
    *,
    base_url: str,
    channel_title: str,
    channel_description: str,
    feed_url: Optional[str],
) -> str:
    # Ensure base_url ends with a slash
    if not base_url.endswith("/"):
        base_url = base_url + "/"

    now = dt.datetime.now(dt.timezone.utc)
    channel_pub_date = format_datetime(items[0]["published_at"]) if items else format_datetime(now)

    xml_parts: List[str] = []
    xml_parts.append("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
    xml_parts.append("<rss version=\"2.0\" xmlns:atom=\"http://www.w3.org/2005/Atom\">")
    xml_parts.append("  <channel>")
    xml_parts.append(f"    <title>{xml_escape(channel_title)}</title>")
    xml_parts.append(f"    <link>{xml_escape(base_url)}</link>")
    xml_parts.append(f"    <description>{xml_escape(channel_description)}</description>")
    xml_parts.append(f"    <lastBuildDate>{xml_escape(channel_pub_date)}</lastBuildDate>")
    if feed_url:
        xml_parts.append(
            f"    <atom:link href=\"{xml_escape(feed_url)}\" rel=\"self\" type=\"application/rss+xml\" />"
        )

    for article in items:
        title = xml_escape(article["title"]) if article["title"] else "Untitled"
        link = base_url + article["rel_url_path"]
        guid = link
        pub_date = format_datetime(article["published_at"])
        description = xml_escape(article["summary"]) if article["summary"] else ""

        xml_parts.append("    <item>")
        xml_parts.append(f"      <title>{title}</title>")
        xml_parts.append(f"      <link>{xml_escape(link)}</link>")
        xml_parts.append(f"      <guid isPermaLink=\"true\">{xml_escape(guid)}</guid>")
        xml_parts.append(f"      <pubDate>{xml_escape(pub_date)}</pubDate>")
        if description:
            xml_parts.append(f"      <description>{description}</description>")
        xml_parts.append("    </item>")

    xml_parts.append("  </channel>")
    xml_parts.append("</rss>")
    return "\n".join(xml_parts) + "\n"


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    md_files = find_markdown_files()
    articles: List[dict] = []
    for path in md_files:
        article = parse_article(path)
        if article is None:
            continue
        articles.append(article)

    # Sort newest first by published_at
    articles.sort(key=lambda a: a["published_at"], reverse=True)
    if args.limit > 0:
        articles = articles[: args.limit]

    if args.verbose:
        for a in articles:
            print(f"+ {a['published_at'].date()} | {a['title']} -> {a['rel_url_path']}")

    # Determine feed self URL
    feed_url = args.feed_url

    rss_xml = build_rss(
        articles,
        base_url=args.base_url,
        channel_title=args.title,
        channel_description=args.description,
        feed_url=feed_url,
    )

    args.output.write_text(rss_xml, encoding="utf-8")
    if args.verbose:
        print(f"Wrote feed with {len(articles)} item(s) to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
