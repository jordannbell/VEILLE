import sys
from datetime import datetime, timezone

import feedparser
import httpx

from common import save_items

FEEDS = [
    {"name": "postgresql-versions", "url": "https://www.postgresql.org/versions.rss", "tags": ["postgresql"]},
    {"name": "cert-fr", "url": "https://www.cert.ssi.gouv.fr/feed/", "tags": ["securite"]},
    {"name": "docker-blog", "url": "https://www.docker.com/feed/", "tags": ["docker"]},
]


def fetch_feed(feed):
    response = httpx.get(
        feed["url"],
        timeout=10,
        follow_redirects=True,
        headers={"User-Agent": "veille/0.1"},
    )
    response.raise_for_status()
    parsed = feedparser.parse(response.content)
    if parsed.bozo and not parsed.entries:
        raise ValueError(f"flux illisible : {parsed.bozo_exception}")
    return parsed.entries


def to_item(feed, entry):
    published = entry.get("published_parsed") or entry.get("updated_parsed")
    published_at = (
        datetime(*published[:6], tzinfo=timezone.utc).isoformat() if published else None
    )
    return {
        "source": f"rss:{feed['name']}",
        "kind": "article",
        "external_id": entry.get("id") or entry.get("link"),
        "title": entry.get("title", "(sans titre)"),
        "url": entry.get("link"),
        "published_at": published_at,
        "summary": (entry.get("summary") or "")[:500],
        "tags": feed["tags"] + ["rss"],
    }


def main():
    items = []
    failures = 0

    for feed in FEEDS:
        try:
            for entry in fetch_feed(feed):
                item = to_item(feed, entry)
                if item["external_id"]:
                    items.append(item)
        except httpx.HTTPError as exc:
            failures += 1
            print(f"[N1] echec reseau rss:{feed['name']} : {exc}", file=sys.stderr)
        except ValueError as exc:
            failures += 1
            print(f"[N2] flux invalide rss:{feed['name']} : {exc}", file=sys.stderr)

    save_items(items)
    print(f"{len(items)} elements deposes, {failures} source(s) en echec")
    if failures == len(FEEDS):
        sys.exit(1)


if __name__ == "__main__":
    main()
