# CLAUDE.md: OperationEpicEval

Read this first. It records the vision, decisions and current state so a new session can pick up without the original conversation.

## What this is
**OperationEpicEval: Evaluation & Awards Ecosystem.** A secure, AI-assisted app where Airmen and Guardians log their work all year. Each unit's award rules are codified, and evaluation and award packages route up the chain in one place.

- **Owner / proposer:** Michael Rosa, 96th Maintenance Squadron (96 MXS), 96 MXG. Michael.Rosa@us.af.mil. The rank isn't recorded yet; ask before adding it.
- **Audience:** the DAF AI Factory at AFRL, for pitch, sponsorship and an IL4/IL5 environment.
- **Two purposes:**
  1. **Product:** give administrative time back to the warfighter. Evaluations and awards are valuable; the hours spent creating, emailing, marking up, re-sending and routing them are not (ADR-0004).
  2. **Pathfinder:** benchmark how fast the DAF can take a gap to an MVP and IOC at IL4/IL5 under today's processes, and document every blocker (ADR-0005).

## The problem, in the owner's words (paraphrased)
Records are rebuilt from memory at the end of the period. PDFs are emailed, opened, marked up, saved and emailed back at every layer. An estimated 60–80% of it happens at the deadline; this is the owner's estimate and a baseline should be measured. The know-how for "promotable records" lives in scattered PDFs and a few supervisors' heads. Example of that know-how: "selected over 5 peers; within 2 weeks in the new role, improved productivity 80%."

## The product: three layers plus one AI assistant
1. **Capture:** the journal. Log jobs, efforts, dates, impact and metrics in about 30 seconds. Entries can feed overlapping periods (quarterly award + annual evaluation).
2. **Context:**
   - **Org tree:** Wing > Group > Squadron > Flight > Section > Element, with roles (CC, SEL, Flight CC/Chief, Supervisor, Board).
   - **Award catalog:** who can apply (a list of org units, optionally narrowed by criteria), format (statement count, max lines, bullet or narrative, sections), rubric, routing, suspense dates, and `advances_to` (the nomination ladder).
   - **SEL setup interview (5–10 min):** maps sub-units, lists awards, ticks eligibility, sets format, routing and dates. Inherits from group and wing; the SEL overrides only what differs. The AI can pre-fill it from an uploaded SOP.
   - **Document library:** writing guides, award SOPs, sanitized past winners and unit priorities, with scope, owner, version and approval. The AI cites sources.
3. **Coordination:** one live package routes member > first supervisor > section chief > flight leadership > SEL > board, with inline comments, tracked edits, return/forward, full history and escalation of overdue items. No email or PDF loop.

**AI roles** (`ai/assist/`): setup-guide, coach, scorer, editor, reviewer-copilot, sanitizer.

## Decisions (do not relitigate without the owner)
| Decision | Where |
|---|---|
| Cloud-agnostic: AWS GovCloud or Azure Government, Kubernetes, Platform One compatible, Iron Bank, FIPS, CAC/PKI, air-gap ready; IL4 baseline, IL5 path | ADR-0001, README portability rules |
| Award rules are versioned data, not code; a cycle pins its rule version | ADR-0002 |
| **AI scores the writing, not the person.** Advisory only; never shown to boards; boards score anonymized packages | ADR-0003 |
| Success = admin time returned to the mission, with records as good or better | ADR-0004 |
| Pathfinder benchmark alongside the product | ADR-0005 |
| **No tiers.** Eligibility is org-scoped (which flights, sections or elements can apply); optional categories are just labels | owner direction, 2026-09-28 |
| Humans decide; the AI never auto-submits; every AI output is logged and traceable | README guardrails |
| The member owns their journal; supervisors see only submitted packages; access follows the rating chain | roles-and-access.md |
| A prep and coordination tool that feeds official systems of record, not a replacement | README |
| Evaluation data is Privacy Act PII: PIA and SORN determination early; EDIPI stored as a hash only | compliance/privacy, schema |
| Example packages must be sanitized and human-approved before sharing (enforced in the schema) | knowledge-library.md |
| PostgreSQL + pgvector as the portable DB and vector store | ADR-0001, schema.sql |

## Reference unit: 96 MXS (public org info only; no personnel data)
- **Munitions Flight**
  - Materiel Section: Storage, Inspection, Operations
  - Production Section: Line Delivery, Conventional Maintenance, PGM
  - Systems Section: Munitions Control, Plans & Scheduling, "Flight" (**name unconfirmed**)
- **PMEL Flight:** sections not mapped yet
- Known award: **Maintenance Professional of the Quarter**, 5 narrative statements, max 6 lines each, advances to 96 MXG. All other award names and formats are **placeholders**.

## Current state (as of 2026-09-29)
- **Built:** folder scaffold with READMEs, architecture docs, ADRs 1–5, draft Postgres schema (`data/schemas/schema.sql`, not yet run against a real database), award-rules example YAML, roadmap, pitch one-pager (md), one-page **project charter PDF**, benchmark-log template.
- **Not built:** no application code, IaC or CI yet.
- **Blueprint page (interactive org chart, routing flow, roadmap):** https://claude.ai/artifact/EtmtHm2o2aB5pv4NDG9MFD (private to the owner). The source is `docs/roadmap-visual/awards-blueprint.html`; republish from that file to keep the link.
- **Charter PDF:** rebuild with `python pitch/src/build_charter.py pitch/project-charter.pdf` in a venv with `pitch/src/requirements.txt`. It must stay one page; the script prints column heights against the space available.

## Roadmap (fiscal quarters)
0. **FY27 Q1 (now):** pitch and clickable prototype on synthetic 96 MXS data.
1. **FY27 Q2:** MVP in a testable IL4 environment.
2. **FY27 Q3:** IOC, 96 MXS pilot with one real quarterly cycle.
3. **FY27 Q4 – FY28 Q1:** group and wing.
4. **FY28+:** enterprise, both clouds, IL5.

Details: `docs/roadmap.md`.

## Open questions for the owner
- Owner's rank for the charter header? DSN?
- Name of the third Systems Section element; PMEL sections
- Real award names, formats and suspense dates (SOPs) for 96 MXS
- Does routing include a section-chief step for every sectioned flight? Do civilians and officers route differently?
- Bullet format, narrative format, or both?
- Proposed team size (2–3 devs + 1 designer, two quarters) OK?
- Keep the repo public, or move it to private or a government-approved repo (e.g., Platform One / Party Bus GitLab)?

## Suggested next steps
1. Build the **clickable prototype** (Phase 0): SEL setup, member drafting with the six-line check and AI coach, supervisor review with AI score. Use synthetic data.
2. Run a quick **baseline survey** (hours per package per role, email round-trips) to replace the 60–80% estimate.
3. Start `docs/pathfinder/benchmark-log.csv` at the first AI Factory contact.
4. Resolve the open questions above and replace placeholders.
5. Deliver the charter to the AI Factory.

## Working conventions for Claude
- **Speak plainly.** The owner is a maintainer and SEL-track leader, not a software engineer. Explain tech terms briefly.
- **Never put CUI, PII, personnel data, secrets or model weights in the repo.** The GitHub repo is **public** (owner's choice, 2026-09-29).
- **Git:** repo at `github.com/CallMeRosaa/OperationEpicEval`, branch `main`. Commit identity is set locally to `Michael Rosa <221785936+CallMeRosaa@users.noreply.github.com>`. Push only when the owner asks.
- **Tools:** Homebrew and `gh` are installed at `/opt/homebrew/bin` (use full paths if PATH isn't loaded). `gh` is logged in as CallMeRosaa.
- **Never type passwords or credentials** for the owner. Sign-ins and sudo prompts are theirs to do.
