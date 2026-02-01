#!/usr/bin/env python3
"""
News collection script for daily digest.
Fetches news from various sources based on interests.yaml configuration.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.parse import quote_plus
import xml.etree.ElementTree as ET

# Try to import yaml, fall back to basic parsing if not available
try:
    import yaml
except ImportError:
    yaml = None


def load_config(config_path: str) -> dict:
    """Load interests.yaml configuration."""
    with open(config_path, 'r', encoding='utf-8') as f:
        if yaml:
            return yaml.safe_load(f)
        else:
            # Basic YAML parsing fallback (limited)
            print("Warning: PyYAML not installed. Using basic parsing.")
            return {}


def fetch_url(url: str, headers: dict = None) -> str:
    """Fetch URL content with error handling."""
    try:
        req = Request(url, headers=headers or {
            'User-Agent': 'Mozilla/5.0 (compatible; DailyDigestBot/1.0)'
        })
        with urlopen(req, timeout=30) as response:
            return response.read().decode('utf-8')
    except (URLError, HTTPError) as e:
        print(f"Error fetching {url}: {e}")
        return ""


def fetch_hacker_news(limit: int = 30) -> list[dict]:
    """Fetch top stories from Hacker News."""
    items = []
    base_url = "https://hacker-news.firebaseio.com/v0"

    # Get top story IDs
    top_ids_json = fetch_url(f"{base_url}/topstories.json")
    if not top_ids_json:
        return items

    top_ids = json.loads(top_ids_json)[:limit]

    for story_id in top_ids:
        story_json = fetch_url(f"{base_url}/item/{story_id}.json")
        if story_json:
            story = json.loads(story_json)
            if story and story.get('type') == 'story':
                items.append({
                    'title': story.get('title', ''),
                    'url': story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                    'score': story.get('score', 0),
                    'source': 'Hacker News',
                    'timestamp': datetime.fromtimestamp(story.get('time', 0), tz=timezone.utc).isoformat()
                })

    return items


def fetch_reddit(subreddits: list[str], limit: int = 10) -> list[dict]:
    """Fetch posts from Reddit subreddits."""
    items = []

    for subreddit in subreddits:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
        content = fetch_url(url)
        if not content:
            continue

        try:
            data = json.loads(content)
            for post in data.get('data', {}).get('children', []):
                post_data = post.get('data', {})
                items.append({
                    'title': post_data.get('title', ''),
                    'url': f"https://reddit.com{post_data.get('permalink', '')}",
                    'score': post_data.get('score', 0),
                    'source': f"Reddit r/{subreddit}",
                    'timestamp': datetime.fromtimestamp(
                        post_data.get('created_utc', 0), tz=timezone.utc
                    ).isoformat()
                })
        except json.JSONDecodeError:
            print(f"Error parsing Reddit response for r/{subreddit}")

    return items


def fetch_rss(url: str, source_name: str, limit: int = 20) -> list[dict]:
    """Fetch items from RSS feed."""
    items = []
    content = fetch_url(url)
    if not content:
        return items

    try:
        root = ET.fromstring(content)
        # Handle both RSS and Atom feeds
        namespaces = {'atom': 'http://www.w3.org/2005/Atom'}

        # Try RSS format
        for item in root.findall('.//item')[:limit]:
            title = item.find('title')
            link = item.find('link')
            pub_date = item.find('pubDate')

            items.append({
                'title': title.text if title is not None else '',
                'url': link.text if link is not None else '',
                'score': 0,
                'source': source_name,
                'timestamp': pub_date.text if pub_date is not None else ''
            })

        # Try Atom format if no RSS items found
        if not items:
            for entry in root.findall('.//atom:entry', namespaces)[:limit]:
                title = entry.find('atom:title', namespaces)
                link = entry.find('atom:link', namespaces)
                updated = entry.find('atom:updated', namespaces)

                items.append({
                    'title': title.text if title is not None else '',
                    'url': link.get('href') if link is not None else '',
                    'score': 0,
                    'source': source_name,
                    'timestamp': updated.text if updated is not None else ''
                })
    except ET.ParseError as e:
        print(f"Error parsing RSS feed {url}: {e}")

    return items


def fetch_arxiv(categories: list[str], keywords: list[str], limit: int = 20) -> list[dict]:
    """Fetch papers from arXiv."""
    items = []

    # Filter out non-ASCII keywords (arXiv only supports ASCII)
    ascii_keywords = [kw for kw in keywords if kw.isascii()]

    if not ascii_keywords:
        print("Warning: No ASCII keywords for arXiv search, using categories only")
        cat_query = " OR ".join([f"cat:{cat}" for cat in categories])
        query = cat_query
    else:
        # Build query
        cat_query = " OR ".join([f"cat:{cat}" for cat in categories])
        keyword_query = " OR ".join([f"all:{kw}" for kw in ascii_keywords[:5]])
        query = f"({cat_query}) AND ({keyword_query})"

    # URL encode the query
    encoded_query = quote_plus(query)
    url = f"https://export.arxiv.org/api/query?search_query={encoded_query}&start=0&max_results={limit}&sortBy=submittedDate&sortOrder=descending"
    content = fetch_url(url)
    if not content:
        return items

    try:
        root = ET.fromstring(content)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}

        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns)
            link = entry.find("atom:link[@title='pdf']", ns)
            if link is None:
                link = entry.find('atom:id', ns)
            summary = entry.find('atom:summary', ns)
            published = entry.find('atom:published', ns)

            items.append({
                'title': title.text.strip().replace('\n', ' ') if title is not None else '',
                'url': link.get('href') if link is not None and link.get('href') else (link.text if link is not None else ''),
                'summary': summary.text.strip()[:500] if summary is not None else '',
                'score': 0,
                'source': 'arXiv',
                'timestamp': published.text if published is not None else ''
            })
    except ET.ParseError as e:
        print(f"Error parsing arXiv response: {e}")

    return items


def filter_by_keywords(items: list[dict], keywords: list[str]) -> list[dict]:
    """Filter items by keywords (case-insensitive)."""
    if not keywords:
        return items

    keywords_lower = [kw.lower() for kw in keywords]
    filtered = []

    for item in items:
        title_lower = item.get('title', '').lower()
        summary_lower = item.get('summary', '').lower()
        text = f"{title_lower} {summary_lower}"

        if any(kw in text for kw in keywords_lower):
            filtered.append(item)

    return filtered


def collect_all(config: dict) -> dict[str, list[dict]]:
    """Collect news from all sources based on config."""
    results = {}
    sources = config.get('sources', {})
    topics = config.get('topics', [])

    # Collect from each source
    all_items = []

    # Hacker News
    if 'hacker_news' in sources:
        print("Fetching Hacker News...")
        hn_items = fetch_hacker_news(limit=50)
        all_items.extend(hn_items)
        print(f"  Found {len(hn_items)} items")

    # Reddit
    if 'reddit' in sources:
        subreddits = sources['reddit'].get('subreddits', [])
        print(f"Fetching Reddit ({', '.join(subreddits)})...")
        reddit_items = fetch_reddit(subreddits, limit=15)
        all_items.extend(reddit_items)
        print(f"  Found {len(reddit_items)} items")

    # TechCrunch RSS
    if 'techcrunch' in sources:
        print("Fetching TechCrunch...")
        tc_items = fetch_rss(sources['techcrunch'].get('url', ''), 'TechCrunch')
        all_items.extend(tc_items)
        print(f"  Found {len(tc_items)} items")

    # arXiv
    if 'arxiv' in sources:
        categories = sources['arxiv'].get('categories', ['cs.AI', 'cs.LG'])
        # Collect keywords from high-priority topics
        keywords = []
        for topic in topics:
            if topic.get('priority') == 'high':
                keywords.extend(topic.get('keywords', []))
        print("Fetching arXiv...")
        arxiv_items = fetch_arxiv(categories, keywords, limit=30)
        all_items.extend(arxiv_items)
        print(f"  Found {len(arxiv_items)} items")

    # Organize by topic
    for topic in topics:
        topic_name = topic.get('name', 'Unknown')
        keywords = topic.get('keywords', [])
        filtered = filter_by_keywords(all_items, keywords)

        # Sort by score (if available) and deduplicate
        seen_urls = set()
        unique_items = []
        for item in sorted(filtered, key=lambda x: x.get('score', 0), reverse=True):
            url = item.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_items.append(item)

        results[topic_name] = unique_items[:config.get('digest', {}).get('max_items_per_topic', 10)]
        print(f"Topic '{topic_name}': {len(results[topic_name])} items")

    return results


def save_raw_data(data: dict, output_path: str):
    """Save collected data as JSON for digest generation."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            'collected_at': datetime.now(timezone.utc).isoformat(),
            'topics': data
        }, f, ensure_ascii=False, indent=2)


def main():
    # Paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    # Config can be in repo or passed as argument
    config_path = sys.argv[1] if len(sys.argv) > 1 else repo_root / 'interests.yaml'
    output_path = repo_root / 'collected_news.json'

    if not Path(config_path).exists():
        # Use template if no config exists
        config_path = repo_root / 'templates' / 'knowledge-base' / 'interests.yaml'

    if not Path(config_path).exists():
        print(f"Error: Config file not found at {config_path}")
        sys.exit(1)

    print(f"Loading config from {config_path}")
    config = load_config(str(config_path))

    if not config:
        print("Error: Failed to load configuration")
        sys.exit(1)

    print("\nCollecting news...")
    data = collect_all(config)

    print(f"\nSaving to {output_path}")
    save_raw_data(data, str(output_path))

    print("\nCollection complete!")


if __name__ == '__main__':
    main()
