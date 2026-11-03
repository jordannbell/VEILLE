CREATE TABLE IF NOT EXISTS veille.digests (
    id          bigserial   PRIMARY KEY,
    day         date        NOT NULL UNIQUE,
    item_count  integer     NOT NULL,
    body_md     text        NOT NULL,
    created_at  timestamptz NOT NULL DEFAULT now()
);
