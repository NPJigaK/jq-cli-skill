---
name: jq-cli
description: Use when Codex needs to inspect, transform, filter, validate, or summarize JSON with the jq CLI, especially for jq filters, JSON/JSONL pipelines, shell quoting, --arg/--argjson values, large inputs, module imports, or exit-status checks.
---

# jq CLI

## Overview

Use `jq` as a command-line JSON processor with explicit attention to shell
quoting, safe argument passing, bounded output, and non-destructive writes.
Prefer small, verified jq commands over ad hoc JSON parsing in shell text tools.

## Workflow

1. Verify the tool when behavior depends on jq features:
   - Run `jq --version`.
   - If jq is missing, stop and ask the user to install it or approve an install
     path. Do not silently replace jq with another parser.
2. Inspect the input shape before writing filters:
   - Determine whether input is one JSON value, multiple JSON texts, JSONL/NDJSON,
     raw text, or generated input.
   - Preview only a small sample for large files.
   - Decide whether downstream steps need one JSON value, JSONL, raw text, or
     only a validation exit status.
3. Choose the right input mode:
   - Normal JSON or JSONL: default jq input is usually correct.
   - No input / construct JSON: use `-n`.
   - Raw lines or non-JSON text: use `-R`; combine with `-s` only when the whole
     file is known to be small enough to hold in memory.
   - Large nested data: consider `--stream` or `reduce inputs` before `-s`.
4. Build the filter safely:
   - Use `.foo` only for identifier-like keys.
   - Use `.["key.with.dots"]` for unusual keys.
   - Pass user strings with `--arg name value`.
   - Pass trusted JSON values with `--argjson name JSON`.
   - Pass files with `--slurpfile name file.json` or `--rawfile name file.txt`.
   - Do not concatenate untrusted user text into a jq filter.
5. Execute with shell-aware quoting:
   - For complex filters, write a temporary `.jq` file and run `jq -f filter.jq`.
   - For shell-specific quoting details, read `references/quoting.md`.
   - For generated, quote-heavy, or file-changing transforms, test on a small
     representative sample before running against the full input.
6. Bound and interpret output:
   - Use `-c` for compact JSON lines.
   - Use `-r` only when the consumer expects raw strings, not JSON.
   - Use `-e` for boolean validation checks and interpret exit statuses.
   - If another command will consume saved output as JSON, validate it with
     `jq empty` when parseability is enough, or a stronger contract check. For
     exactly one JSON value, include an input-count check such as `jq -s -e`.
   - Avoid dumping huge transformed JSON into the chat; write to a file or show a
     capped preview.
7. Write files safely:
   - Never redirect to the same file being read.
   - Write to a temporary file, validate it with jq, then replace the target.
   - Preserve the original until validation succeeds.

## Common Patterns

Extract a field:

```bash
jq '.items[].name' input.json
```

Filter by a user-provided string:

```bash
jq --arg status "active" '.items[] | select(.status == $status)' input.json
```

Validate a condition with exit status:

```bash
jq -e 'all(.items[]; has("id"))' input.json
```

Use a filter file for anything quote-heavy:

```bash
jq -f transform.jq input.json > output.tmp
jq empty output.tmp
```

Safely rewrite a JSON file:

```bash
jq '.items |= sort_by(.id)' data.json > data.json.tmp
jq -s -e 'length == 1' data.json.tmp > /dev/null
mv data.json.tmp data.json
```

## References

- Read `references/execution.md` for input modes, output modes, exit statuses,
  and write-safety patterns.
- Read `references/quoting.md` before running quote-heavy filters in
  PowerShell, cmd.exe, POSIX shells, or CI YAML.
- Read `references/gotchas.md` for precision, module/import, JSONL, memory, and
  secret-leak hazards.
