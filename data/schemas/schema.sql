-- Draft PostgreSQL schema (portable: RDS / Azure Database for PostgreSQL / in-cluster)
-- PII columns are marked. Encrypt at rest with a customer-managed key.

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE member (
  id            UUID PRIMARY KEY,
  edipi_hash    TEXT UNIQUE NOT NULL,   -- PII: store a hash only, mapped from the CAC
  display_name  TEXT NOT NULL,          -- PII
  rank_grade    TEXT,
  unit          TEXT,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE assignment (
  id         UUID PRIMARY KEY,
  member_id  UUID NOT NULL REFERENCES member(id),
  title      TEXT NOT NULL,             -- duty title / job
  unit       TEXT,
  start_date DATE NOT NULL,
  end_date   DATE
);

CREATE TABLE rating_chain_link (
  id            UUID PRIMARY KEY,
  member_id     UUID NOT NULL REFERENCES member(id),
  reviewer_id   UUID NOT NULL REFERENCES member(id),
  role          TEXT NOT NULL CHECK (role IN ('SUPERVISOR','RATER','ADDITIONAL_RATER','REVIEWER')),
  start_date    DATE NOT NULL,
  end_date      DATE
);

CREATE TABLE rating_period (
  id          UUID PRIMARY KEY,
  member_id   UUID NOT NULL REFERENCES member(id),
  type        TEXT NOT NULL CHECK (type IN ('QUARTERLY_AWARD','SEMIANNUAL','ANNUAL_EVAL','CUSTOM')),
  label       TEXT NOT NULL,            -- e.g. "FY27 Q1 Award", "2027 Annual Eval"
  start_date  DATE NOT NULL,
  end_date    DATE NOT NULL,
  status      TEXT NOT NULL DEFAULT 'OPEN' CHECK (status IN ('OPEN','DRAFTING','IN_REVIEW','CLOSED'))
);

CREATE TABLE entry (
  id             UUID PRIMARY KEY,
  member_id      UUID NOT NULL REFERENCES member(id),
  assignment_id  UUID REFERENCES assignment(id),
  occurred_on    DATE NOT NULL,
  occurred_end   DATE,                  -- for multi-day efforts
  title          TEXT NOT NULL,
  action         TEXT,                  -- what I did
  impact         TEXT,                  -- so what / result
  metrics        JSONB,                 -- {"hours_saved": 120, "dollars": 45000, ...}
  tags           TEXT[],
  embedding      vector(1024),          -- for search and AI retrieval; dimension set by the chosen model
  created_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE attachment (
  id          UUID PRIMARY KEY,
  entry_id    UUID NOT NULL REFERENCES entry(id) ON DELETE CASCADE,
  object_key  TEXT NOT NULL,            -- S3 / Blob key via the storage provider adapter
  filename    TEXT NOT NULL,
  sha256      TEXT NOT NULL
);

CREATE TABLE bullet (
  id          UUID PRIMARY KEY,
  member_id   UUID NOT NULL REFERENCES member(id),
  style       TEXT NOT NULL CHECK (style IN ('BULLET','NARRATIVE')),
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE bullet_version (
  id          UUID PRIMARY KEY,
  bullet_id   UUID NOT NULL REFERENCES bullet(id) ON DELETE CASCADE,
  text        TEXT NOT NULL,
  author_type TEXT NOT NULL CHECK (author_type IN ('MEMBER','AI','REVIEWER')),
  author_id   UUID REFERENCES member(id),
  model_id    TEXT,                     -- which model and version, if AI
  accepted    BOOLEAN NOT NULL DEFAULT false,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE bullet_source (            -- traceability: bullet <-> entries
  bullet_id UUID REFERENCES bullet(id) ON DELETE CASCADE,
  entry_id  UUID REFERENCES entry(id)  ON DELETE CASCADE,
  PRIMARY KEY (bullet_id, entry_id)
);

CREATE TABLE package (
  id               UUID PRIMARY KEY,
  rating_period_id UUID NOT NULL REFERENCES rating_period(id),
  kind             TEXT NOT NULL CHECK (kind IN ('AWARD','EVALUATION')),
  award_name       TEXT,
  status           TEXT NOT NULL DEFAULT 'DRAFT' CHECK (status IN ('DRAFT','SUBMITTED_FOR_REVIEW','CHANGES_REQUESTED','APPROVED','EXPORTED'))
);

CREATE TABLE package_item (
  package_id  UUID REFERENCES package(id) ON DELETE CASCADE,
  bullet_id   UUID REFERENCES bullet(id),
  section     TEXT,                     -- award category or performance area
  position    INT NOT NULL,
  PRIMARY KEY (package_id, bullet_id)
);

CREATE TABLE review (
  id          UUID PRIMARY KEY,
  package_id  UUID NOT NULL REFERENCES package(id) ON DELETE CASCADE,
  reviewer_id UUID NOT NULL REFERENCES member(id),
  comment     TEXT,
  decision    TEXT CHECK (decision IN ('COMMENT','CHANGES_REQUESTED','APPROVED')),
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE audit_event (              -- AU family; append-only
  id          BIGSERIAL PRIMARY KEY,
  actor_id    UUID,
  action      TEXT NOT NULL,
  object_type TEXT NOT NULL,
  object_id   UUID,
  detail      JSONB,
  at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ON entry (member_id, occurred_on);
CREATE INDEX ON rating_period (member_id, start_date, end_date);
