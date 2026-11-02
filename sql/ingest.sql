BEGIN ISOLATION LEVEL REPEATABLE READ;

INSERT INTO veille.items
    (content_hash, source, kind, title, url, published_at, summary, tags)
SELECT
    encode(sha256(convert_to((payload->>'source') || '|' || (payload->>'external_id'), 'UTF8')), 'hex'),
    payload->>'source',
    payload->>'kind',
    payload->>'title',
    payload->>'url',
    (payload->>'published_at')::timestamptz,
    payload->>'summary',
    ARRAY(SELECT jsonb_array_elements_text(payload->'tags'))
FROM veille.raw_items
WHERE NOT processed
ON CONFLICT (content_hash) DO NOTHING;

UPDATE veille.raw_items SET processed = true WHERE NOT processed;

COMMIT;
