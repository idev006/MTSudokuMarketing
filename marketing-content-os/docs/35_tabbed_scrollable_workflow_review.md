# Desktop Pipeline Tabbed + Scrollable Workflow Review

Status: ACTIVE UX REVIEW
Date: 2026-08-25
Scope: `marketing-content-os/apps/social_pipeline_desktop`

## User request

The user correctly identified that the desktop workflow had become complex enough that a single large screen was no longer the best interaction pattern.

Requested direction:

- split the complex workflow into tabs; or
- make sections scrollable; or
- both.

## UX decision

The app should use both:

1. an always-visible Command Bar for the main operator actions;
2. a tabbed workflow for conceptual separation;
3. scrollable tab contents so smaller screens remain usable.

## Implemented tab model

The desktop app now uses these tabs:

```text
1. GPT1 Request
2. Import & Clean
3. Results
4. GPT2 Handoff
5. Review
```

This maps directly to the production workflow:

```text
SKU + N -> GPT1 -> raw files -> deterministic clean/validate -> GPT2 prompts -> image + review
```

## Why this is better

| Before | After |
|---|---|
| Many controls visible in one large panel | Controls grouped by task |
| User had to visually scan the whole screen | User can follow tabs left-to-right |
| Resizable panels helped but still felt busy | Tabs reduce cognitive load |
| Command Bar existed but context was spread out | Command Bar remains global and tabs provide context |
| Smaller screens were still crowded | Each tab is scrollable |

## Command Bar policy

The Command Bar remains visible above the tabs:

```text
Copy GPT1 Prompt
Choose Raw Folder
Run Pipeline
Open _cleaned Folder
Reset
```

Policy:

- major commands must remain visible;
- unavailable commands should be disabled, not hidden;
- tabs should explain the context of each command;
- the workflow must still answer: "What should I do now?"

## Process engineering boundary

No production boundary changed:

- GPT1 still starts the workflow;
- the desktop app only performs deterministic clean/validate/output preparation;
- GPT2 handoff remains controlled;
- image generation and human review remain separate gates;
- no auto-publish and no bypass of human review.

## Review result

This is a better fit for a Level 3 operator cockpit.

The updated UI now supports:

- task separation;
- scrollable content;
- always-visible command access;
- lower cognitive load;
- clearer operator navigation;
- dynamic `1 <= N <= 60` workflow continuity.
