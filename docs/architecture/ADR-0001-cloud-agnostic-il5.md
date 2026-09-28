# ADR-0001: Cloud-agnostic architecture targeting IL4/IL5

**Status:** Proposed

## Context
The application must be pitched to the AFRL DAF AI Factory and be deployable into IL4/IL5 on either AWS GovCloud or Azure Government.

## Decision
- Kubernetes (EKS/AKS) is the runtime, with Helm and Kustomize overlays for each cloud and impact level.
- Terraform modules share one interface, with separate `aws` and `azure` implementations.
- A provider-adapter pattern in the backend isolates cloud services (storage, secrets, queue, LLM).
- PostgreSQL with pgvector is the portable database and vector store.
- Iron Bank images, FIPS crypto, and air-gap packaging (Zarf) are used from day one.

## Consequences
Managed-service features that only exist on one cloud are avoided unless wrapped behind an adapter.
