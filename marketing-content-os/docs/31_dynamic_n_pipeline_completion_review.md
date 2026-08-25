# Dynamic N Pipeline Completion Review

Status: PILOT COMPLETE
Date: 2026-08-25
Scope: `marketing-content-os/apps/social_pipeline_desktop`

## 1. Review objective

Verify that the desktop pipeline now supports operator-defined post count `N` while preserving the document-driven project rule and downstream usability.

## 2. Requirement reviewed

User requirement:

```text
ผู้ใช้สามารถกำหนดจำนวนรายการเป็น N เมื่อ 1<=N<=60
ต้องเขียนเอกสารของโครงการให้เป็นไปตามหลักการทำโครงการระดับโลก document driven project, project must follow document.
output โปรแกรมต้องนำไปใช้ต่อได้ อย่างถูกต้อง มีประสิทธิภาพ และ ง่าย
```

## 3. Implemented behavior

The app now exposes `Post count N` in the UI.

```text
MIN_POST_COUNT = 1
MAX_POST_COUNT = 60
DEFAULT_POST_COUNT = 10
```

The same N is used as:

```text
GPT1 NUMBER_OF_ROWS=N
Cleaner expected_rows=N
Selected rows target=N
GPT2 prompt target=N
```

## 4. Document-driven control

Added controlling SSOT document:

```text
marketing-content-os/docs/30_dynamic_n_social_pipeline_contract.md
```

Updated operational app documentation:

```text
marketing-content-os/apps/social_pipeline_desktop/README.md
```

The contract defines N range, SIPOC, process map, stage gates, output contract, downstream usability requirements, UX requirements, and automation boundary.

## 5. Output review

For each selected folder, expected output is:

```text
_cleaned/
  clean/
    <raw_file>_clean.tsv
  reports/
    <raw_file>_clean_report.json
  selected/
    <raw_file>_selected_<N>.tsv
  handoff/
    <raw_file>/
      01_<ROW_ID>_gpt2_prompt.txt
      ...
      NN_<ROW_ID>_gpt2_prompt.txt
    <raw_file>_handoff_index.tsv
  pipeline_batch_summary.json
```

The output is downstream-ready because:

- clean TSV is the canonical validated handoff artifact;
- report JSON is diagnosable;
- selected TSV matches the rows used for prompt generation;
- each GPT2 prompt file contains exactly one `MODE: TEMPLATE_HANDOFF` request;
- handoff index provides ordered prompt navigation;
- batch summary provides run-level traceability.

## 6. User experience review

The operator journey is reduced to:

```text
1. Set N
2. Use GPT1 prompt skeleton
3. Save GPT1 raw files
4. Choose Folder
5. Clean All Files + Prepare N GPT2 Prompts
6. Copy/open GPT2 prompts
```

The user does not need to know TSV internals or command-line cleaner arguments.

## 7. Controlled limitations

The app still does not:

- run GPT1 automatically;
- run GPT2 automatically;
- generate images automatically;
- publish automatically;
- bypass human review.

These are intentional quality gates.

## 8. Acceptance conclusion

The implementation satisfies the requested Level 3 workflow direction for pilot use:

```text
1 <= N <= 60
project documentation controls behavior
code follows the documented process
outputs are usable by GPT2 and reviewers
operator workload is reduced
```
