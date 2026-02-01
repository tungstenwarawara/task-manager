#!/usr/bin/env python3
"""
Convert collected news JSON to Markdown format.
No API required - just formats the raw data.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def json_to_markdown(data: dict) -> str:
    """Convert collected news data to Markdown format."""
    collected_at = data.get('collected_at', datetime.now(timezone.utc).isoformat())
    topics = data.get('topics', {})

    lines = [
        f"# Daily News - {datetime.now().strftime('%Y-%m-%d')}",
        "",
        f"> Collected at: {collected_at}",
        "",
    ]

    for topic_name, items in topics.items():
        if not items:
            continue

        lines.append(f"## {topic_name}")
        lines.append("")

        for item in items[:10]:  # Limit to 10 items per topic
            title = item.get('title', 'No title')
            url = item.get('url', '')
            source = item.get('source', '')
            score = item.get('score', 0)
            summary = item.get('summary', '')

            # Format as list item with link
            if url:
                lines.append(f"- [{title}]({url})")
            else:
                lines.append(f"- {title}")

            # Add metadata
            meta = []
            if source:
                meta.append(f"Source: {source}")
            if score:
                meta.append(f"Score: {score}")
            if meta:
                lines.append(f"  - {' | '.join(meta)}")

            # Add summary if available
            if summary:
                lines.append(f"  - {summary[:200]}...")

            lines.append("")

        lines.append("")

    lines.append("---")
    lines.append("*This is raw collected data. Ask Claude Code to summarize: 「今日のダイジェストを要約して」*")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 3:
        print("Usage: news-to-markdown.py <input.json> <output_dir>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])

    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    # Create output directory structure
    today = datetime.now()
    year_dir = output_dir / str(today.year)
    month_dir = year_dir / f"{today.month:02d}"
    month_dir.mkdir(parents=True, exist_ok=True)

    output_path = month_dir / f"{today.day:02d}.md"

    # Load and convert
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    markdown = json_to_markdown(data)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown)

    print(f"Saved to {output_path}")


if __name__ == '__main__':
    main()
