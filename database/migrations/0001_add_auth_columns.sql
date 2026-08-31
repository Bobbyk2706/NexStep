-- Adds the columns the auth module needs to the EXISTING student and admin
-- tables. No new user table is created — auth reads/writes these two.
--
-- account_status: student didn't have this column before; admin already
--   did. Login is blocked only when it's explicitly 'suspended',
--   'inactive', or 'disabled' — NULL/'active' both mean active, so
--   existing rows keep working without a backfill.
-- token_version: opaque string embedded in every refresh token's "trv"
--   claim. Refresh/logout rotate it, which invalidates older refresh
--   tokens. NULL is fine for pre-existing rows; it's set on next login.

ALTER TABLE student
    ADD COLUMN IF NOT EXISTS account_status VARCHAR(20) DEFAULT 'active',
    ADD COLUMN IF NOT EXISTS token_version VARCHAR(64);

ALTER TABLE admin
    ADD COLUMN IF NOT EXISTS token_version VARCHAR(64);