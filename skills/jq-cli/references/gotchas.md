# jq Gotchas for Agents

Use this before large, security-sensitive, or correctness-sensitive jq work.

## JSONL Is Not One Array

JSONL/NDJSON is a stream of JSON texts, not necessarily an array. Default jq
can process it one JSON value at a time:

```bash
jq '.id' records.jsonl
```

Only use `-s` when you actually need all records in memory at once.

## `-r` Changes the Contract

`-r` emits raw strings. That is useful for shell tools, but it is no longer JSON
output. Do not use `-r` when the next step expects valid JSON.

## Multiple Outputs Are Normal

Many jq filters emit multiple JSON values:

```bash
jq '.items[].id' input.json
```

If the consumer expects one JSON value, wrap results:

```bash
jq '[.items[].id]' input.json
```

## Missing Keys Produce `null`

`.foo` on an object without `foo` yields `null`. For validation, use `has`,
explicit comparisons, and `-e`:

```bash
jq -e 'has("foo") and (.foo != null)' input.json
```

## Successful jq Can Still Have the Wrong Contract

Parsing and exit code `0` do not prove the output is suitable for the next step.
Before passing jq output to another command, decide whether the contract is one
JSON value, JSONL, raw text, or only a validation exit status. Save important
outputs to a temp file and validate that contract explicitly.

## Precision Can Matter

jq number handling can preserve decimal literals in some cases, but arithmetic
can convert to IEEE754 double precision. Treat IDs, money, and high-precision
numbers as strings when exact representation matters.

## Modules and Imports Read Files

jq supports modules and imports. Search paths can include user-level locations
such as `~/.jq`, and a home-directory `.jq` file can be automatically sourced.

For untrusted repositories or filters:

- inspect `import` and `include` directives
- prefer explicit `-L` paths for known modules
- avoid running unknown jq modules against sensitive input

## Environment and Secret Leakage

jq can access environment data through builtins such as `$ENV` and `env`.
Avoid printing whole environments or passing secrets through jq output unless
the user explicitly asks.

## Output and Memory Explosions

Watch for filters that multiply data:

- broad `.[]` expansion on large arrays
- nested generators that create cartesian products
- `sort`, `group_by`, `unique`, and `-s` on huge streams
- recursive descent `..` over large documents
- unbounded `range`, recursion, or `while`

For big inputs, prefer streaming reductions and capped previews.

## Time and Locale Functions Vary

Date/time functions can depend on platform C library behavior. If exact
cross-platform timestamp handling matters, test on the target platform.
