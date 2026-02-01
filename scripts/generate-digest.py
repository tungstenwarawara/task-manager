#!/usr/bin/env python3
"""
Digest generation script using Claude API.
Reads collected news and generates a summarized digest.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Try to import anthropic
try:
    import anthropic
except ImportError:
    anthropic = None


def load_collected_news(input_path: str) -> dict:
    """Load collected news from JSON file."""
    with open(input_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def format_items_for_prompt(topics: dict) -> str:
    """Format collected items for the Claude prompt."""
    formatted = []

    for topic_name, items in topics.items():
        if not items:
            continue

        formatted.append(f"\n## {topic_name}\n")
        for i, item in enumerate(items[:15], 1):  # Limit items per topic
            formatted.append(f"{i}. **{item.get('title', 'No title')}**")
            formatted.append(f"   - Source: {item.get('source', 'Unknown')}")
            formatted.append(f"   - URL: {item.get('url', '')}")
            if item.get('summary'):
                formatted.append(f"   - Summary: {item['summary'][:200]}...")
            formatted.append("")

    return "\n".join(formatted)


def generate_digest_with_claude(collected_data: dict, api_key: str) -> str:
    """Use Claude API to generate a summarized digest."""
    if not anthropic:
        print("Warning: anthropic package not installed. Generating basic digest.")
        return generate_basic_digest(collected_data)

    client = anthropic.Anthropic(api_key=api_key)

    topics_text = format_items_for_prompt(collected_data.get('topics', {}))

    prompt = f"""以下は今日収集されたニュース・記事のリストです。これを日本語で要約し、読みやすいダイジェストを作成してください。

要件:
1. 各トピックごとに重要なニュースを3-5件選んでください
2. 各ニュースは1-2文で簡潔に要約してください
3. 元のURLへのリンクを含めてください
4. 特に注目すべきニュースがあれば「今日のハイライト」として最初にまとめてください
5. Markdown形式で出力してください

収集されたニュース:
{topics_text}

ダイジェストを生成してください:"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text
    except Exception as e:
        print(f"Error calling Claude API: {e}")
        return generate_basic_digest(collected_data)


def generate_basic_digest(collected_data: dict) -> str:
    """Generate a basic digest without AI summarization."""
    lines = []
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    lines.append(f"# Daily Digest - {today}\n")
    lines.append("*Note: AI summarization unavailable. Showing raw collected items.*\n")

    for topic_name, items in collected_data.get('topics', {}).items():
        if not items:
            continue

        lines.append(f"\n## {topic_name} ({len(items)}件)\n")

        for item in items[:10]:
            title = item.get('title', 'No title')
            url = item.get('url', '')
            source = item.get('source', 'Unknown')

            lines.append(f"### {title}")
            lines.append(f"- Source: {source}")
            if url:
                lines.append(f"- [Read more]({url})")
            lines.append("")

    lines.append("---")
    lines.append(f"*Generated: {datetime.now(timezone.utc).isoformat()}*")

    return "\n".join(lines)


def save_digest(content: str, output_dir: str, date: datetime = None):
    """Save digest to markdown file with date-based path."""
    if date is None:
        date = datetime.now(timezone.utc)

    # Create directory structure: digest/YYYY/MM/DD.md
    year_dir = Path(output_dir) / str(date.year)
    month_dir = year_dir / f"{date.month:02d}"
    month_dir.mkdir(parents=True, exist_ok=True)

    output_file = month_dir / f"{date.day:02d}.md"

    # Add header if not present
    if not content.startswith("# Daily Digest"):
        header = f"# Daily Digest - {date.strftime('%Y-%m-%d')}\n\n"
        content = header + content

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Digest saved to {output_file}")
    return str(output_file)


def main():
    # Paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    input_path = sys.argv[1] if len(sys.argv) > 1 else repo_root / 'collected_news.json'
    output_dir = sys.argv[2] if len(sys.argv) > 2 else repo_root / 'digest'

    if not Path(input_path).exists():
        print(f"Error: Input file not found at {input_path}")
        print("Run collect-news.py first.")
        sys.exit(1)

    print(f"Loading collected news from {input_path}")
    collected_data = load_collected_news(str(input_path))

    # Get API key from environment
    api_key = os.environ.get('ANTHROPIC_API_KEY', '')

    print("\nGenerating digest...")
    if api_key:
        digest = generate_digest_with_claude(collected_data, api_key)
    else:
        print("Warning: ANTHROPIC_API_KEY not set. Generating basic digest.")
        digest = generate_basic_digest(collected_data)

    print(f"\nSaving digest to {output_dir}")
    output_file = save_digest(digest, str(output_dir))

    print("\nDigest generation complete!")
    print(f"Output: {output_file}")


if __name__ == '__main__':
    main()
