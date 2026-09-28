# AFRL DAF AI Factory — Evaluation & Awards Ecosystem (working name)

> **Use case:** A secure, year-round workspace where Airmen and Guardians log their jobs, efforts, accomplishments and dates as they happen. They then turn those notes, with AI help, into bullets, narrative statements, award packages and evaluation inputs for any rating period (quarterly award, semi-annual, or annual evaluation).

## Problem
Accomplishments get recalled from memory at the end of the period. That causes lost details, missing metrics, last-minute scrambles for supervisors, and uneven quality between members.

## Core flow
```
Log entry (anytime, 30 sec) ─▶ Rating period ─▶ Bullets / statements (AI-assisted, human-approved)
                                              ─▶ Award package / evaluation draft ─▶ Supervisor review ─▶ Export
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
- **AI drafts, humans decide.** Nothing is auto-submitted, and every AI suggestion can be traced to the member's own entries.
- **Prep tool, not system of record.** Official evaluations and awards still go through the official systems. This app feeds them.

## Layout
| Folder | Purpose |
|---|---|
| `app/backend/src/core/` | `periods`, `entries`, `bullets`, `packages`, `reviews`, `export` |
| `ai/` | `assist` (bullet writing), models, inference, RAG, prompts, evals, guardrails |
| `data/` | Schemas (`schemas/schema.sql`), migrations, synthetic data |
| `infra/` | Terraform (AWS/Azure), Kubernetes, containers, air-gap bundling |
| `pipelines/`, `.github/` | CI/CD (DevSecOps) |
| `security/` | SBOMs, scanners, STIGs, signing |
| `compliance/` | RMF/ATO, **privacy (PIA/SORN)**, AI risk |
| `docs/` | ADRs, domain model, runbooks, user guides |
| `pitch/` | AI Factory one-pager and demo |
