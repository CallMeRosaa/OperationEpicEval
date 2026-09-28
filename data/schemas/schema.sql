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

-- ===== Org structure =====
CREATE TABLE org_unit (
  id         UUID PRIMARY KEY,
  parent_id  UUID REFERENCES org_unit(id),
  level      TEXT NOT NULL CHECK (level IN ('WING','GROUP','SQUADRON','FLIGHT','SECTION')),
  name       TEXT NOT NULL
);

CREATE TABLE unit_context (              -- mission and priorities; used by the AI
  org_unit_id UUID PRIMARY KEY REFERENCES org_unit(id),
  mission     TEXT,
  priorities  TEXT[],
  updated_by  UUID REFERENCES member(id),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE unit_role_assignment (
  id          UUID PRIMARY KEY,
  org_unit_id UUID NOT NULL REFERENCES org_unit(id),
  member_id   UUID NOT NULL REFERENCES member(id),
  role        TEXT NOT NULL CHECK (role IN ('COMMANDER','SEL','FLIGHT_CC','FLIGHT_CHIEF','SUPERVISOR','BOARD','ADMIN')),
  start_date  DATE NOT NULL,
  end_date    DATE
);

CREATE TABLE supervision (               -- who is whose first supervisor
  member_id     UUID NOT NULL REFERENCES member(id),
  supervisor_id UUID NOT NULL REFERENCES member(id),
  start_date    DATE NOT NULL,
  end_date      DATE,
  PRIMARY KEY (member_id, supervisor_id, start_date)
);

-- ===== Award catalog & rules =====
CREATE TABLE award_program (
  id           UUID PRIMARY KEY,
  org_unit_id  UUID NOT NULL REFERENCES org_unit(id),   -- owner level (wing template or unit override)
  code         TEXT NOT NULL,
  name         TEXT NOT NULL,
  cadence      TEXT NOT NULL CHECK (cadence IN ('QUARTERLY','SEMIANNUAL','ANNUAL','AD_HOC')),
  advances_to  UUID REFERENCES award_program(id),
  overrides_id UUID REFERENCES award_program(id),       -- unit override of a group/wing award
  categories   TEXT[]                                    -- optional labels the unit uses, e.g. {Airman,NCO,SNCO,Civilian}
);

CREATE TABLE award_eligibility (          -- "who can apply": which org units, optionally narrowed
  id                UUID PRIMARY KEY,
  award_program_id  UUID NOT NULL REFERENCES award_program(id) ON DELETE CASCADE,
  org_unit_id       UUID NOT NULL REFERENCES org_unit(id),
  includes_subunits BOOLEAN NOT NULL DEFAULT true,
  criteria          JSONB                -- optional, e.g. {"duty_titles_any":["Inspector"]}
);

CREATE TABLE award_rule_version (
  id               UUID PRIMARY KEY,
  award_program_id UUID NOT NULL REFERENCES award_program(id),
  version          INT NOT NULL,
  rules            JSONB NOT NULL,       -- format, sections, statement counts, max lines, line_fit
  rubric           JSONB NOT NULL,       -- scoring criteria and weights (AI scorer + board)
  created_by       UUID REFERENCES member(id),
  created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (award_program_id, version)
);

CREATE TABLE routing_template (
  id          UUID PRIMARY KEY,
  org_unit_id UUID NOT NULL REFERENCES org_unit(id),
  name        TEXT NOT NULL,
  steps       JSONB NOT NULL             -- [{"role":"FIRST_SUPERVISOR","action":"REVIEW","can_return":true},...]
);

CREATE TABLE award_cycle (
  id                  UUID PRIMARY KEY,
  award_program_id    UUID NOT NULL REFERENCES award_program(id),
  rule_version_id     UUID NOT NULL REFERENCES award_rule_version(id),  -- pinned
  routing_template_id UUID NOT NULL REFERENCES routing_template(id),
  label               TEXT NOT NULL,     -- "FY27 Q1"
  period_start        DATE NOT NULL,
  period_end          DATE NOT NULL,
  status              TEXT NOT NULL DEFAULT 'OPEN' CHECK (status IN ('SETUP','OPEN','ROUTING','BOARD','CLOSED'))
);

CREATE TABLE cycle_milestone (
  id             UUID PRIMARY KEY,
  award_cycle_id UUID NOT NULL REFERENCES award_cycle(id) ON DELETE CASCADE,
  step_role      TEXT NOT NULL,
  label          TEXT NOT NULL,          -- "Drafts due to flight leadership"
  due_at         TIMESTAMPTZ NOT NULL
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
  member_id        UUID NOT NULL REFERENCES member(id),
  kind             TEXT NOT NULL CHECK (kind IN ('NOMINATION','EVALUATION')),
  award_cycle_id   UUID REFERENCES award_cycle(id),     -- nominations
  rating_period_id UUID REFERENCES rating_period(id),   -- evaluations
  category         TEXT,                                -- optional, from award_program.categories
  current_step     INT NOT NULL DEFAULT 0,              -- index into routing template steps
  current_holder   UUID REFERENCES member(id),          -- whose inbox it is in
  status           TEXT NOT NULL DEFAULT 'DRAFT' CHECK (status IN
                     ('DRAFT','IN_ROUTING','RETURNED','NOMINATED','AT_BOARD','WON','NOT_SELECTED','EXPORTED','WITHDRAWN')),
  CHECK ((kind = 'NOMINATION' AND award_cycle_id IS NOT NULL) OR (kind = 'EVALUATION' AND rating_period_id IS NOT NULL))
);

CREATE TABLE package_item (
  package_id  UUID REFERENCES package(id) ON DELETE CASCADE,
  bullet_id   UUID REFERENCES bullet(id),
  section     TEXT,                     -- award category or performance area
  position    INT NOT NULL,
  PRIMARY KEY (package_id, bullet_id)
);

-- ===== Coordination =====
CREATE TABLE routing_event (             -- append-only history
  id          BIGSERIAL PRIMARY KEY,
  package_id  UUID NOT NULL REFERENCES package(id) ON DELETE CASCADE,
  step_index  INT NOT NULL,
  actor_id    UUID NOT NULL REFERENCES member(id),
  action      TEXT NOT NULL CHECK (action IN ('SUBMIT','FORWARD','RETURN','APPROVE','NOMINATE','WITHDRAW','ESCALATE')),
  to_member   UUID REFERENCES member(id),
  note        TEXT,
  at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE comment (
  id                UUID PRIMARY KEY,
  package_id        UUID NOT NULL REFERENCES package(id) ON DELETE CASCADE,
  bullet_version_id UUID REFERENCES bullet_version(id),
  anchor            JSONB,               -- {"start":12,"end":40} text span
  parent_id         UUID REFERENCES comment(id),
  author_id         UUID NOT NULL REFERENCES member(id),
  body              TEXT NOT NULL,
  resolved          BOOLEAN NOT NULL DEFAULT false,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE ai_assessment (             -- advisory; never shown to boards (ADR-0003)
  id              UUID PRIMARY KEY,
  package_id      UUID NOT NULL REFERENCES package(id) ON DELETE CASCADE,
  requested_by    UUID NOT NULL REFERENCES member(id),
  rule_version_id UUID NOT NULL REFERENCES award_rule_version(id),
  scores          JSONB NOT NULL,        -- {"impact":{"score":4,"reason":"..."}, ...}
  overall         NUMERIC(3,1),
  model_id        TEXT NOT NULL,
  prompt_version  TEXT NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE board_score (
  id          UUID PRIMARY KEY,
  package_id  UUID NOT NULL REFERENCES package(id),
  board_member UUID NOT NULL REFERENCES member(id),
  scores      JSONB NOT NULL,
  total       NUMERIC(5,1) NOT NULL,
  UNIQUE (package_id, board_member)
);

-- ===== Knowledge library =====
CREATE TABLE library_document (
  id            UUID PRIMARY KEY,
  scope_unit_id UUID REFERENCES org_unit(id),   -- NULL when personal
  owner_id      UUID NOT NULL REFERENCES member(id),
  personal      BOOLEAN NOT NULL DEFAULT false,
  doc_type      TEXT NOT NULL CHECK (doc_type IN ('WRITING_GUIDE','AWARD_SOP','EXAMPLE_PACKAGE','UNIT_CONTEXT','PRIOR_RECORD','OTHER')),
  title         TEXT NOT NULL,
  object_key    TEXT NOT NULL,
  sha256        TEXT NOT NULL,
  version       INT NOT NULL DEFAULT 1,
  supersedes_id UUID REFERENCES library_document(id),
  status        TEXT NOT NULL DEFAULT 'DRAFT' CHECK (status IN ('DRAFT','APPROVED','RETIRED')),
  sanitized     BOOLEAN NOT NULL DEFAULT false,  -- required true for EXAMPLE_PACKAGE before APPROVED
  approved_by   UUID REFERENCES member(id),
  uploaded_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
  CHECK (personal OR scope_unit_id IS NOT NULL),
  CHECK (doc_type <> 'EXAMPLE_PACKAGE' OR status <> 'APPROVED' OR sanitized)
);

CREATE TABLE document_chunk (
  id           BIGSERIAL PRIMARY KEY,
  document_id  UUID NOT NULL REFERENCES library_document(id) ON DELETE CASCADE,
  page         INT,
  text         TEXT NOT NULL,
  embedding    vector(1024)
);

-- ===== Time-in-step instrumentation (ADR-0004) =====
CREATE VIEW package_step_durations AS
SELECT package_id, step_index, actor_id, action, at,
       at - LAG(at) OVER (PARTITION BY package_id ORDER BY at) AS time_in_previous_step
FROM routing_event;

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
CREATE INDEX ON package (current_holder, status);
CREATE INDEX ON org_unit (parent_id);
CREATE INDEX ON award_eligibility (org_unit_id);
CREATE INDEX ON cycle_milestone (due_at);
