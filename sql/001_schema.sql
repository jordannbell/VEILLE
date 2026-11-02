CREATE SCHEMA IF NOT EXISTS veille;

-- Boîte de réception : ce que les collecteurs déposent, brut
CREATE TABLE IF NOT EXISTS veille.raw_items (
    id          bigserial   PRIMARY KEY,
    source      text        NOT NULL,
    fetched_at  timestamptz NOT NULL DEFAULT now(),
    payload     jsonb       NOT NULL,
    processed   boolean     NOT NULL DEFAULT false
);

-- Table propre : une ligne par élément unique
CREATE TABLE IF NOT EXISTS veille.items (
    id            bigserial   PRIMARY KEY,
    content_hash  text        NOT NULL UNIQUE,
    source        text        NOT NULL,
    kind          text        NOT NULL,
    title         text        NOT NULL,
    url           text,
    published_at  timestamptz,
    summary       text,
    tags          text[]      NOT NULL DEFAULT '{}',
    first_seen_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_items_first_seen
    ON veille.items (first_seen_at DESC);
