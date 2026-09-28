# AFRL DAF AI Factory — [Project Name TBD]

> **Use case:** _TBD — one sentence on the mission problem, the user, and the measurable outcome._

## Deployment targets
| Environment | AWS | Azure | Data |
|---|---|---|---|
| dev / demo | Commercial or GovCloud | Commercial or Azure Gov | Synthetic only |
| IL4 | AWS GovCloud (US) | Azure Government | CUI |
| IL5 | AWS GovCloud (US), IL5 PA | Azure Government (DoD regions), IL5 PA | CUI + NSS |

## Portability rules (non-negotiable)
1. **No cloud SDKs outside `app/backend/src/providers/`.** Core logic stays cloud-agnostic.
2. **Kubernetes-first.** EKS or AKS, deployed with Helm and Kustomize. Compatible with Platform One Big Bang.
3. **Iron Bank base images only.** Pin every image by digest.
4. **FIPS 140-validated crypto.** Use FIPS endpoints, TLS 1.2+, and customer-managed KMS or Key Vault keys.
5. **Air-gap ready.** No runtime calls to the public internet, public CDNs, or SaaS. Every dependency is mirrored.
6. **CAC/PKI authentication** plus RBAC/ABAC. Every AI interaction goes to the audit log.
7. **No CUI, PII, secrets, or model weights in git.**

## Layout
| Folder | Purpose |
|---|---|
| `app/` | Backend API + frontend |
| `ai/` | Models, inference, RAG, prompts, evals, guardrails |
| `data/` | Schemas, migrations, synthetic data |
| `infra/` | Terraform (AWS/Azure), Kubernetes, containers, air-gap bundling |
| `pipelines/`, `.github/` | CI/CD (DevSecOps) |
| `security/` | SBOMs, scanners, STIGs, signing |
| `compliance/` | RMF/ATO: SSP, 800-53 controls, CRM, AI risk, diagrams, POA&M |
| `docs/` | ADRs, runbooks, user guides |
| `pitch/` | AI Factory pitch materials and demo |

Each folder has a README describing what belongs there.
