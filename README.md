# AFRL DAF AI Factory — Evaluation & Awards Ecosystem (working name)

> **Use case:** A secure, year-round workspace where Airmen and Guardians log their jobs, efforts, accomplishments and dates as they happen. They then turn those notes, with AI help, into bullets, narrative statements, award packages and evaluation inputs for any rating period (quarterly award, semi-annual, or annual evaluation).

## Problem
Accomplishments get recalled from memory at the end of the period. That causes lost details, missing metrics, last-minute scrambles for supervisors, and uneven quality between members.

## Three layers
1. **Capture.** Members journal what they did, when, and the impact, all year.
2. **Context.** Each unit's award catalog is codified: tiers, format rules (e.g., 5 statements, 6 lines max), rubric, routing chain and suspense dates. It also holds unit mission and priorities. The SEL stands this up in a 10-15 minute guided setup, inheriting from a wing template.
3. **Coordination.** Packages route member > first supervisor > flight leadership > SEL > board, with inline comments, tracked edits, return and forward, and deadline tracking.

An **AI assistant** works across all three: it coaches the member, scores the writing against the award rubric, suggests edits, and helps supervisors review. It is advisory only, and humans make every decision.

```
Journal ─▶ Pick award (eligible tier auto-detected) ─▶ Draft (rules checked live, AI coach)
        ─▶ Supervisor ⇄ member (comments, AI score, tracked edits) ─▶ Flight ─▶ SEL ─▶ Board
```

## Deployment targets
| Environment | AWS | Azure | Data |
|---|---|---|---|
| dev / demo | Commercial or GovCloud | Commercial or Azure Gov | Synthetic only |
| IL4 | AWS GovCloud (US) | Azure Government | CUI / PII (**expected baseline**) |
| IL5 | AWS GovCloud (US), IL5 PA | Azure Government (DoD regions), IL5 PA | CUI + NSS |

## Portability rules (non-negotiable)
1. **No cloud SDKs outside `app/backend/src/providers/`.** Core logic stays cloud-agnostic.
2. **Kubernetes-first.** EKS or AKS, deployed with Helm and Kustomize. Compatible with Platform One Big Bang.
3. **Iron Bank base images only.** Pin every image by digest.
4. **FIPS 140-validated crypto.** Use FIPS endpoints, TLS 1.2+, and customer-managed KMS or Key Vault keys.
5. **Air-gap ready.** No runtime calls to the public internet, public CDNs, or SaaS. Every dependency is mirrored.
6. **CAC/PKI authentication** plus RBAC/ABAC. Every AI interaction goes to the audit log.
7. **No CUI, PII, secrets, or model weights in git.**

## Product guardrails
- **The member owns their journal.** Supervisors see only what is shared with them, following the rating chain.
- **AI scores the writing, not the person.** AI scores are coaching feedback and are never shown to boards (ADR-0003).
- **AI drafts, humans decide.** Nothing is auto-submitted, and every AI suggestion can be traced to the member's own entries.
- **Prep tool, not system of record.** Official evaluations and awards still go through the official systems. This app feeds them.

## Layout
| Folder | Purpose |
|---|---|
| `app/backend/src/core/` | `org`, `awards`, `cycles`, `admin`, `entries`, `periods`, `bullets`, `packages`, `routing`, `formatting`, `export` |
| `ai/` | `assist/{coach, scorer, editor, reviewer-copilot}`, models, inference, RAG, prompts, evals, guardrails |
| `data/` | Schemas (`schemas/schema.sql`), migrations, synthetic data |
| `config/award-rules/` | Award rules as data: wing template example (fictional 999 TW) |
| `infra/` | Terraform (AWS/Azure), Kubernetes, containers, air-gap bundling |
| `pipelines/`, `.github/` | CI/CD (DevSecOps) |
| `security/` | SBOMs, scanners, STIGs, signing |
| `compliance/` | RMF/ATO, **privacy (PIA/SORN)**, AI risk |
| `docs/` | ADRs, domain model, runbooks, user guides |
| `pitch/` | AI Factory one-pager and demo |
