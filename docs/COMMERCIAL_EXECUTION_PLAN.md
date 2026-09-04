# BidCheck Commercial Execution Plan

## Current position

P1 is functionally advanced and P3 API foundations exist, but P1 is not declared PASS until the real end-to-end gate is executed successfully. P2 provider infrastructure exists as groundwork; it is not considered complete.

## Remaining execution rounds

1. **P1 Gate** — run real TXT/PDF/DOCX/XLSX ingestion, requirement extraction, response matching, evidence/risk output, report generation and negative-path tests. PASS requires the complete workflow to execute without manual code intervention.
2. **P2 AI audit** — production-grade provider interface, timeout/retry/cost accounting, structured semantic judgement, evidence grounding, confidence validation and deterministic fallback to rules/review.
3. **P3 Product API/Web** — authenticated project/document/audit/report workflow, user/tenant isolation, persistent task state, upload handling and a usable web workflow.
4. **P4 Monetization** — plans, quotas, usage metering, subscription/order abstraction, entitlement enforcement and payment integration boundary.
5. **P5 Production** — PostgreSQL migration path, object storage abstraction, background jobs, observability, rate limiting, security hardening, Docker deployment and operational documentation.
6. **P6 Commercial MVP + final gate** — landing page, onboarding, pricing, trial, paid workflow, report export, help docs, production smoke test and final commercial audit.

## Completion rule

The product is complete when a new user can register, create a project, upload real bidding materials, receive an evidence-backed audit result and understand how to pay. Non-blocking improvements become backlog after each gate; they must not block progression.
