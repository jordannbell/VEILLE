import argparse
from collections import defaultdict
from datetime import date

import psycopg

from common import DSN


def build_markdown(day, rows):
    lines = [f"# Veille du {day}", "", f"{len(rows)} nouveaute(s)", ""]
    by_source = defaultdict(list)
    for source, title, url, published_at in rows:
        by_source[source].append((title, url, published_at))
    for source in sorted(by_source):
        entries = by_source[source]
        lines.append(f"## {source} ({len(entries)})")
        for title, url, published_at in entries:
            when = published_at.date().isoformat() if published_at else "date inconnue"
            lines.append(f"- [{title}]({url}) - {when}")
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hours", type=int, default=24)
    args = parser.parse_args()

    today = date.today()
    with psycopg.connect(DSN) as conn:
        rows = conn.execute(
            """
            SELECT source, title, url, published_at
            FROM veille.items
            WHERE first_seen_at >= now() - make_interval(hours => %s)
            ORDER BY source, published_at DESC NULLS LAST
            """,
            (args.hours,),
        ).fetchall()
        body = build_markdown(today, rows)
        conn.execute(
            """
            INSERT INTO veille.digests (day, item_count, body_md)
            VALUES (%s, %s, %s)
            ON CONFLICT (day) DO UPDATE
            SET item_count = EXCLUDED.item_count,
                body_md = EXCLUDED.body_md,
                created_at = now()
            """,
            (today, len(rows), body),
        )
    print(body)


if __name__ == "__main__":
    main()
