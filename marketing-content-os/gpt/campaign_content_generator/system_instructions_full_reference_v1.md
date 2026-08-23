# BiiigBee Campaign Content Generator v1.0-rc1 — Full Reference Index

This document points maintainers to the expanded design/reference material behind the compact GPT Builder instructions. It is **NOT** the text to paste into the GPT Builder Instructions field.

Use the compact canonical Builder instructions at:
`marketing-content-os/gpt/campaign_content_generator/system_instructions_v1.md`

Detailed behavior and rationale remain documented in the Content OS contracts, schemas, taxonomy, prompt registry, lookup contract, manifest, acceptance tests, and validator.

## Expanded reference sources
- `marketing-content-os/docs/12_input_output_contract.md`
- `marketing-content-os/docs/13_system_instruction_quality_gates.md`
- `marketing-content-os/docs/14_shared_marketing_brain_contract.md`
- `marketing-content-os/docs/16_controlled_vocabulary.md`
- `marketing-content-os/docs/17_prompt_lookup_contract.md`
- `marketing-content-os/docs/18_version_manifest_contract.md`
- `marketing-content-os/docs/19_tsv_serialization_contract.md`
- `marketing-content-os/docs/20_large_batch_protocol.md`
- `marketing-content-os/docs/21_deterministic_validator_spec.md`
- `marketing-content-os/tests/campaign_content_generator_acceptance_corpus_v1.tsv`
- `marketing-content-os/tests/acceptance_execution_rubric_v1.md`

## Purpose
- keep the Builder Instructions safely below the 8,000-character limit
- preserve detailed governance outside the runtime instruction field
- prevent duplicate or conflicting runtime rules
- support future revisions and regression review

## Governance
Runtime behavior is governed by the compact canonical Builder instructions plus the approved Knowledge bundle. Any material runtime change must first be reflected in GitHub, checked for instruction-length compliance, versioned as appropriate, and retested.
