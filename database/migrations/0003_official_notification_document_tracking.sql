-- Adds the exact document identity fields required by the monitoring
-- pipeline. They are populated from the approved official PDF URL and
-- its SHA-256 hash, so monitoring always checks the exact document that
-- was reviewed rather than a generic official webpage.

ALTER TABLE officialnotification
    ADD COLUMN IF NOT EXISTS document_url TEXT,
    ADD COLUMN IF NOT EXISTS document_hash VARCHAR(64);
