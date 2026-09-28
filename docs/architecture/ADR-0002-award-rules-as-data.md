# ADR-0002: Award rules are configuration, not code

**Status:** Proposed

**Context:** Every wing and squadron runs different awards, eligibility, formats and suspense dates, and they change each year.

**Decision:** Award programs, eligibility (org units + optional criteria), format constraints, routing templates and cycle milestones are versioned data (YAML/JSON schema, stored in the DB). A wing template is inherited by units, and the SEL overrides it through a guided setup. Each cycle pins the rule version it was created with.

**Consequences:** Onboarding a new unit takes minutes and needs no deployment. The rules engine and line-fit engine must be generic.
