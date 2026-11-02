import os

import psycopg
from psycopg.types.json import Jsonb

DSN = os.environ.get(
    "VEILLE_DB_DSN", "postgresql://veille:veille_dev@localhost:5432/veille"
)


def save_items(items):
    """Depose les elements dans la boite de reception veille.raw_items."""
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            for item in items:
                cur.execute(
                    "INSERT INTO veille.raw_items (source, payload) VALUES (%s, %s)",
                    (item["source"], Jsonb(item)),
                )
