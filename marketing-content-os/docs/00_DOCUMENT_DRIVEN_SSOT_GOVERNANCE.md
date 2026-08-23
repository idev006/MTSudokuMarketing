# BiiigBee Marketing Content OS — Document-Driven SSOT Governance

Status: ACTIVE / MANDATORY
Effective: 2026-08-23

## 1. Governing Principle
This project is document-driven. Approved project documents in the GitHub repository are the operational Source of Truth (SSOT).

Chat messages, model memory, temporary notes, generated prose, and assumptions are not authoritative by themselves. Any material decision that changes product truth, architecture, schema, taxonomy, GPT behavior, acceptance criteria, release status, workflow, or production process must be recorded in the repository before it is treated as project truth.

## 2. Required Working Rule
Project execution MUST follow the current approved documents.

When implementation, GPT configuration, code, tests, or chat guidance conflicts with approved documentation:
1. stop the conflicting action;
2. identify the conflicting sources;
3. update/approve the governing document first when a change is intended;
4. update dependent code/config/tests/artifacts to match;
5. rerun affected validation or acceptance tests;
6. record the resulting status/evidence.

Do not silently let code, GPT Builder configuration, or chat become a parallel source of truth.

## 3. SSOT Hierarchy
Unless a more specific contract states otherwise, use this precedence:
1. approved product/SKU source-of-truth documents;
2. approved architecture/contracts/governance documents;
3. approved schemas, controlled vocabularies, registries, and manifests;
4. approved GPT system instructions/configuration documents;
5. acceptance corpus, rubrics, status/evidence records;
6. implementation code and generated artifacts;
7. safe explicit user instruction that does not conflict with higher-priority approved truth;
8. model assumptions.

A material conflict inside the highest applicable tier is blocking. Do not guess a winner.

## 4. Documentation Before/With Change
For every material change, maintain at least one durable record covering:
- decision/change summary;
- reason;
- affected contracts/files;
- version impact;
- validation/acceptance impact;
- current status;
- evidence or commit/PR reference when available.

Documentation may be updated in the same PR as implementation, but it must not be deferred indefinitely after implementation.

## 5. Mandatory Continuously-Maintained Records
The following records must stay current:
- `marketing-content-os/README.md` — current system/release state and next gate;
- `marketing-content-os/knowledge_manifest_v1.yaml` — deployed knowledge/runtime version references;
- `marketing-content-os/tests/acceptance_execution_status_v1.md` — smoke/full acceptance status and evidence;
- GPT Builder configuration/instruction documents under `marketing-content-os/gpt/`;
- relevant schemas/taxonomy/registries/contracts when behavior changes;
- this governance document when SSOT/process rules change.

## 6. Evidence Rule
A test is not complete because a GPT says it passed. Acceptance evidence must be based on the actual emitted rows/output and the applicable deterministic validator/audit plus semantic/human review defined by the project rubric.

Failures, warnings, regressions, and mitigations must be recorded in the acceptance status document or another linked durable project record.

## 7. Release Rule
No component may be promoted to Production solely from chat agreement or informal testing. Release status must follow documented release gates and recorded acceptance evidence.

For GPT #1, `TC-001..TC-032` and the documented deterministic + semantic gates govern production eligibility.

For GPT #2, production eligibility remains blocked until GPT #1's row contract is accepted/frozen and GPT #2's documented acceptance tests pass.

## 8. Change-Control Checklist
Before closing a material change:
- [ ] governing docs updated;
- [ ] dependent code/config aligned;
- [ ] manifest/version impact evaluated;
- [ ] affected tests rerun or explicitly marked pending;
- [ ] status/evidence recorded;
- [ ] no undocumented parallel truth remains in GPT Builder or chat.

## 9. Current Project Directive
BiiigBee Marketing Content OS is formally operated as a **Document-Driven Project with GitHub documentation as SSOT**. Future development, GPT configuration, testing, acceptance, and release work must follow this rule.
