#!/usr/bin/env python3
"""
track-doc-fetch.py - Helper script to track documentation fetches

Usage:
    # As a standalone tracker
    python track-doc-fetch.py add --url "https://docs.sonarsource.com/..." --file tracking.json
    
    # Get summary
    python track-doc-fetch.py summary --file tracking.json
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any
from urllib.parse import urlparse

# Constants
TRACKING_FILE_PATH_KEY = 'Tracking file path'


def load_tracking_file(file_path: Path) -> Dict[str, Any]:
    """Load or create tracking file"""
    if file_path.exists():
        with open(file_path, 'r') as f:
            return json.load(f)
    else:
        return {'fetches': []}


def save_tracking_file(file_path: Path, data: Dict[str, Any]):
    """Save tracking file"""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)


def add_fetch(file_path: Path, url: str, title: str = None, duration_ms: int = None):
    """Add a documentation fetch to tracking"""
    data = load_tracking_file(file_path)
    
    fetch_entry = {
        'url': url,
        'title': title or '',
        'timestamp': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        'fetch_duration_ms': duration_ms
    }
    
    data['fetches'].append(fetch_entry)
    save_tracking_file(file_path, data)
    
    print(f"✓ Tracked fetch: {url}")


def get_summary(file_path: Path) -> Dict[str, Any]:
    """Get summary of documentation fetches"""
    data = load_tracking_file(file_path)
    fetches = data.get('fetches', [])
    
    if not fetches:
        return {
            'total_count': 0,
            'pages': [],
            'domains': [],
            'unique_pages': 0
        }
    
    # Extract domains
    domains = []
    for fetch in fetches:
        url = fetch.get('url', '')
        try:
            parsed = urlparse(url)
            if parsed.hostname:
                domains.append(parsed.hostname)
        except Exception:
            pass
    
    unique_domains = list(set(domains))
    unique_urls = list(set(f['url'] for f in fetches))
    
    return {
        'total_count': len(fetches),
        'pages': fetches,
        'domains': unique_domains,
        'unique_pages': len(unique_urls)
    }


def print_summary(file_path: Path):
    """Print summary to console"""
    summary = get_summary(file_path)
    
    print(f"\n📚 Documentation Fetch Summary")
    print(f"{'=' * 50}")
    print(f"Total Fetches: {summary['total_count']}")
    print(f"Unique Pages: {summary['unique_pages']}")
    print(f"Domains: {', '.join(summary['domains']) if summary['domains'] else 'None'}")
    print(f"{'=' * 50}\n")
    
    if summary['pages']:
        print("Pages Fetched:")
        for i, page in enumerate(summary['pages'], 1):
            url = page.get('url', 'unknown')
            title = page.get('title', '')
            timestamp = page.get('timestamp', '')
            
            print(f"{i:2}. {url}")
            if title:
                print(f"    Title: {title}")
            if timestamp:
                print(f"    Time: {timestamp}")
            print()


def export_summary(file_path: Path, output_path: Path):
    """Export summary to JSON file"""
    summary = get_summary(file_path)
    
    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"✓ Summary exported to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Track documentation fetches')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Add fetch command
    add_parser = subparsers.add_parser('add', help='Add a documentation fetch')
    add_parser.add_argument('--url', required=True, help='URL of the fetched page')
    add_parser.add_argument('--title', help='Page title')
    add_parser.add_argument('--duration', type=int, help='Fetch duration in milliseconds')
    add_parser.add_argument('--file', required=True, help=TRACKING_FILE_PATH_KEY)
    
    # Summary command
    summary_parser = subparsers.add_parser('summary', help='Show fetch summary')
    summary_parser.add_argument('--file', required=True, help=TRACKING_FILE_PATH_KEY)
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export summary to JSON')
    export_parser.add_argument('--file', required=True, help=TRACKING_FILE_PATH_KEY)
    export_parser.add_argument('--output', required=True, help='Output file path')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    file_path = Path(args.file)
    
    if args.command == 'add':
        add_fetch(file_path, args.url, args.title, args.duration)
    elif args.command == 'summary':
        print_summary(file_path)
    elif args.command == 'export':
        export_path = Path(args.output)
        export_summary(file_path, export_path)


if __name__ == '__main__':
    main()
