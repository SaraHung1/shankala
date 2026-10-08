-- Migration 0001: core tables for the Shankala site.
-- Cloudflare D1 runs SQLite, so types follow SQLite conventions.

CREATE TABLE IF NOT EXISTS menu_items (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name_en       TEXT    NOT NULL,
    name_zh       TEXT    NOT NULL,
    description   TEXT    NOT NULL DEFAULT '',
    category      TEXT    NOT NULL CHECK (category IN ('snack', 'drink', 'dessert')),
    price_cents   INTEGER CHECK (price_cents IS NULL OR price_cents >= 0), -- NULL = price not shown
    is_spicy      INTEGER NOT NULL DEFAULT 0 CHECK (is_spicy IN (0, 1)),
    is_available  INTEGER NOT NULL DEFAULT 1 CHECK (is_available IN (0, 1)),
    sort_order    INTEGER NOT NULL DEFAULT 0,
    created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS events (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    location    TEXT NOT NULL,
    starts_on   TEXT NOT NULL,  -- ISO date, e.g. '2027-08-14'
    ends_on     TEXT NOT NULL,
    url         TEXT,
    CHECK (ends_on >= starts_on)
);

CREATE INDEX IF NOT EXISTS idx_events_ends_on ON events (ends_on);

CREATE TABLE IF NOT EXISTS contact_messages (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    email       TEXT NOT NULL,
    topic       TEXT NOT NULL CHECK (topic IN ('general', 'catering', 'event')),
    message     TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_contact_created_at ON contact_messages (created_at);
