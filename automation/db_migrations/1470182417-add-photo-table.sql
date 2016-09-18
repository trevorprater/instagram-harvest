CREATE TABLE photo (
    id BIGINT NOT NULL PRIMARY KEY,
    pcode TEXT NOT NULL UNIQUE,
    owner_id BIGINT NOT NULL,
    location_id BIGINT NOT NULL DEFAULT -1,
    caption TEXT,
    likes BIGINT NOT NULL DEFAULT 0,
    comments BIGINT NOT NULL DEFAULT 0,
    created BIGINT NOT NULL,
    updated BIGINT NOT NULL DEFAULT extract(epoch from (now() at time zone 'utc')::timestamptz(0))::bigint,
    is_vid BOOLEAN NOT NULL DEFAULT FALSE,
    url TEXT NOT NULL UNIQUE
);

