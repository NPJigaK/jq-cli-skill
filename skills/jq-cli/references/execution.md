# jq CLI Execution Reference

Use this when a jq task depends on input mode, output format, exit status, or
safe file writes.

## Preconditions

- Run `jq --version` when the task depends on jq 1.7+ or 1.8+ features.
- Do not assume jq is installed in remote CI, containers, or minimal Windows
  environments.
- If installing jq, prefer the user's package manager or official binaries.

## Input Modes

| Input | Prefer | Notes |
| --- | --- | --- |
| One JSON value | `jq 'filter' file.json` | Default mode parses JSON and runs the filter. |
| Multiple JSON texts / JSONL | `jq 'filter' file.jsonl` | jq can read a stream of JSON texts. |
| Construct JSON | `jq -n 'filter'` | Runs once with `null` input. |
| Raw text lines | `jq -R 'filter' file.txt` | Each line becomes a string. |
| Small whole-file text | `jq -Rs 'filter' file.txt` | Reads the entire file as one string. |
| Small whole JSON stream | `jq -s 'filter' file.jsonl` | Reads all inputs into one array. Avoid for large files. |
| Huge nested JSON | `jq --stream 'filter' file.json` | Emits path/value events; design the filter for streaming form. |

For reductions over many JSON inputs, use `jq -n 'reduce inputs as $x (...; ...)'`
so the first input is not consumed before `inputs`.

## Safe Argument Passing

Never splice user values into the jq program text.

```bash
jq --arg key "customer.id" '.[$key]' input.json
jq --arg status "active" '.items[] | select(.status == $status)' input.json
jq --argjson limit 25 '.items[:$limit]' input.json
jq --slurpfile allowlist allowlist.json '.items[] | select(.id as $id | $allowlist[0] | index($id))' input.json
jq --rawfile body message.txt '.message = $body' input.json
```

Use `--argjson` only for text that is intended to be valid JSON. If the value is
from a user and should be treated as text, use `--arg`.

## Sample and Contract Checks

For generated filters, quote-heavy filters, or transforms whose output will
replace a file or feed another command, test the command on representative input
before the full run. A jq command can parse and still produce the wrong contract:
multiple JSON texts, raw strings, `null`, or a larger output than expected.

Validate the saved output against the consumer's contract, not just syntax:

```bash
jq 'map({id, name})' input.json > output.tmp
jq -s -e 'length == 1 and (.[0] | type == "array" and all(.[]; has("id") and has("name")))' output.tmp > /dev/null
```

The `-s` form above rejects extra top-level JSON texts before handing the file
to a consumer that expects exactly one JSON value. If parseability of a JSON
stream is the only contract, `jq empty output.tmp` is enough.

## Output Modes

| Need | Option | Notes |
| --- | --- | --- |
| Normal JSON | default | Pretty-printed JSON. |
| JSONL / compact | `-c` | One JSON value per line. |
| Raw strings | `-r` | Use only when the next tool expects text, not JSON. |
| NUL-delimited raw strings | `--raw-output0` | Useful with `xargs -0`; fails if output contains NUL. |
| No color | `-M` | Use for logs, files, or tests. |
| No trailing newline | `-j` | Rare; use only when the consumer requires it. |

Do not paste massive stdout into the final answer. Write full output to a file
and summarize a capped preview.

## Exit Status

Without `-e`, a successful jq program can exit `0` even if the final value is
`false` or `null`.

Use `-e` for checks:

| Case with `-e` | Exit |
| --- | ---: |
| Last output is neither `false` nor `null` | 0 |
| Last output is `false` or `null` | 1 |
| No output | 4 |
| Usage/system error | 2 |
| jq compile error | 3 |

Example:

```bash
jq -e 'all(.items[]; has("id"))' input.json
```

## Safe File Writes

Never write directly to the file being read:

```bash
# Wrong: can truncate input before jq reads it.
jq '.items |= sort_by(.id)' data.json > data.json
```

Use a temp file and validate before replacing:

```bash
jq '.items |= sort_by(.id)' data.json > data.json.tmp
jq empty data.json.tmp
mv data.json.tmp data.json
```

On Windows, use the same idea with PowerShell commands. Use the following
redirect pattern in PowerShell 7.4+ or another byte-preserving shell. Windows
PowerShell 5.1 and PowerShell 7.3 or older treat redirected native stdout as
text rather than preserving the original byte stream; Windows PowerShell 5.1
commonly writes UTF-16 output that `jq` may not parse on the validation step.

```powershell
jq '.items |= sort_by(.id)' data.json > data.json.tmp
jq empty data.json.tmp
Move-Item -LiteralPath data.json.tmp -Destination data.json -Force
```

In Windows PowerShell 5.1, run the redirect in `cmd.exe`, a POSIX shell, or
PowerShell 7.4+. Prefer `jq -f transform.jq ... > data.json.tmp` when changing
shells to avoid nested quoting mistakes.

For valuable files, copy a backup or rely on git before replacing.

## Validation Snippets

Parse-only validation:

```bash
jq empty file.json
```

Ensure every object has a key:

```bash
jq -e 'all(.[]; has("id"))' file.json
```

Count JSONL records:

```bash
jq -cn 'reduce inputs as $x (0; . + 1)' file.jsonl
```
