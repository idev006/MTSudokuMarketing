# BiiigBee Campaign Content Generator v1.0-rc1 — Full Reference Instructions

This document preserves the expanded design/reference version of the Campaign Content Generator instructions. It is NOT the text to paste into the GPT Builder Instructions field.

Use the compact canonical Builder instructions at:
`marketing-content-os/gpt/campaign_content_generator/system_instructions_v1.md`

The compact file is the deployment source of truth for the GPT Builder Instructions field. Detailed behavior remains documented across the Content OS contracts, schemas, taxonomy, prompt registry, lookup contract, manifest, acceptance tests, and validator.

## Purpose of this reference file
- retain expanded rationale and implementation notes outside the 8,000-character Builder limit
- support maintainers during future revisions
- prevent the GPT Builder Instructions field from becoming overloaded with reference material
- keep deployment instructions concise while preserving governance documentation in GitHub

## Governance
If this reference file and the compact canonical Builder instructions differ, runtime behavior is governed by the compact canonical Builder instructions plus the approved Knowledge bundle. Any material runtime change must be reflected in the compact file, versioned, and retested.
