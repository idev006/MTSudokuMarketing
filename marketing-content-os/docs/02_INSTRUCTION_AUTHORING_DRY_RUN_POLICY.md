# Instruction Authoring Dry-Run Policy

Status: ACTIVE / MANDATORY
Effective: 2026-08-23
Scope: GPT Builder Instructions, runtime instruction documents, and any future instruction files under `marketing-content-os/gpt/`.

## Purpose

Before changing GPT instructions, the maintainer must internally dry-run the proposed instructions against the affected acceptance behavior instead of relying only on textual intuition. The goal is to catch likely deterministic, serialization, product-truth, and semantic failures before committing and asking for a live Builder rerun.

## Required pre-commit dry-run loop

For every material instruction change:

1. Identify affected acceptance cases and known open defects.
2. Mentally simulate the proposed instruction behavior against those cases, focusing on actual emitted rows, not only policy wording.
3. Check the simulated output against deterministic hard gates: exact row count, 27 fields, column-specific controlled tokens, blank `IMAGE_PROMPT` in Formula mode, template mapping, stable `CAMPAIGN_ID`, global `SEQUENCE`, product grounding, and claim safety.
4. Check semantic/commercial quality: audience fit, campaign coherence, diversity, copy usability, and absence of internal governance language in customer-facing fields.
5. Iterate the proposed instruction wording until the simulated behavior is expected to pass the affected gates, or until a blocker is found.
6. Hard cap: do not exceed 1,000 internal dry-run iterations for one instruction-change campaign. Stop earlier once the expected result is good enough to justify a real rerun.

## Stop conditions

Stop and do not promote the instruction change as ready when:

- an affected deterministic hard gate is still expected to fail;
- product truth or claim safety remains ambiguous;
- the instruction text no longer fits the live GPT Builder limit;
- the change creates conflict with a higher-priority SSOT document;
- 1,000 dry-run iterations are reached without an expected pass.

## Evidence requirement

The private step-by-step reasoning does not need to be written to the repository. However, the PR or evidence record must summarize:

- affected tests/defects considered;
- final dry-run outcome: expected pass, expected warning, blocker, or max-iteration stop;
- notable residual risks, if any;
- whether the live Builder rerun is still required.

## Important limitation

Dry-run simulation is not acceptance evidence. A real GPT Builder rerun, deterministic validation, and semantic/human review remain required before advancing the acceptance gate.
