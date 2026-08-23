# 19 — TSV Serialization Contract v1

## Purpose
Make Content Rows machine-copyable and safe for Google Sheets, validators, and future automation.

## Physical-Line Rule
Each content row must occupy exactly one physical line in TSV output.

## Field Escaping
Before serialization:
- literal TAB inside a field -> single space
- CR (`\r`) -> remove
- physical newline (`\n`) inside a field -> two literal characters `\\n`
- leading/trailing whitespace -> trim
- do not add TSV quoting as a second escaping system

Emoji and normal Unicode/Thai text are allowed.

## Header
The TSV header is exactly the 27 canonical field names in schema order.

## Blank Values
Only fields explicitly allowed by the contract may be blank. In v1 Formula Mode, `IMAGE_PROMPT` is blank by design.

## Round-Trip Requirement
A valid serialized batch must satisfy:
- physical data-line count = NUMBER_OF_ROWS
- every data line splits into exactly 27 TAB-separated fields
- no embedded physical newline exists inside a row
- decoding literal `\\n` for human presentation must not alter column count

## Validation Errors
Hard fail on:
- wrong column count
- malformed header/order
- physical row count mismatch
- embedded TAB that causes >27 columns
- embedded newline that breaks a row into multiple physical records

## Human Copy Guidance
Long captions remain one TSV line. Literal `\\n` may later be converted to a visual line break after import if desired.
