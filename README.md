# jq CLI Agent Skill

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Latest release](https://img.shields.io/github/v/release/NPJigaK/jq-cli-skill?label=release)](https://github.com/NPJigaK/jq-cli-skill/releases/latest)

A portable Agent Skill for using the `jq` command-line JSON processor safely
and reliably from Codex, Claude Code, Cursor, and other SKILL.md-compatible
coding agents.

## Why Use It

Agents can write useful jq commands, but the failure modes are sharp: shell
quoting changes across environments, JSONL is easy to treat as one array, user
values can accidentally become jq program text, and file rewrites can destroy
the input before validation.

This skill gives agents a small workflow for jq work: inspect the input shape,
choose the right jq mode, pass values as data, keep quoting shell-aware, bound
output, and rewrite files through a validated temporary result.

## Quick Start

```bash
npx skills add NPJigaK/jq-cli-skill --skill jq-cli --agent codex
```

```text
$jq-cli Inspect this JSON file and summarize the top-level shape.
```

The same skill works with Codex, Claude Code, Cursor, and other Agent Skills
clients. For Claude Code, Cursor, global installs, no-install usage, and manual
agent prompts, see [INSTALL.md](INSTALL.md).

The installable Skill is:

```text
skills/jq-cli/
```

Install that directory as a whole. Do not install the repository root as a
Skill, and do not copy only `SKILL.md`; the `references/` directory is part of
the runtime guidance.

## Usage

```text
$jq-cli Use jq to extract every .items[].id from data.json.
$jq-cli In PowerShell, read the key foo.bar from input.json.
$jq-cli Sort .items by .id and write the result back safely.
```

## What It Covers

- shell quoting across POSIX shells, PowerShell, and cmd.exe
- passing user values with `--arg`, `--argjson`, `--slurpfile`, and `--rawfile`
- avoiding accidental in-place truncation
- choosing safe input modes for JSON, JSONL, raw text, and large files
- interpreting `jq -e` exit statuses for validation checks
- avoiding module/import, environment-leak, memory, and precision surprises

## Why This Skill Is Written This Way

This section maps the common failure modes to the primary-source behavior that
drives the skill.

### Failure mode: treating jq input as one JSON blob

> "jq filters run on a stream of JSON data."
> - [jq 1.8 manual](https://jqlang.org/manual/v1.8/)

Skill response: inspect whether the input is one JSON value, multiple JSON
texts, JSONL/NDJSON, raw text, or generated input before choosing the jq mode.

### Failure mode: writing a filter for the wrong shell

> "mind the shell's quoting rules."
> - [jq 1.8 manual](https://jqlang.org/manual/v1.8/)

> "parsing continues in argument mode."
> - [PowerShell about_Parsing](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_parsing)

> "A string enclosed in single quotation marks is a verbatim string."
> - [PowerShell about_Quoting_Rules](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_quoting_rules)

Skill response: keep shell-specific examples in `references/quoting.md`, and
prefer `jq -f filter.jq` for complex, generated, or quote-heavy jq programs.

### Failure mode: turning user values into jq program text

> "This option passes a value to the jq program as a predefined variable."
> - [jq 1.8 manual](https://jqlang.org/manual/v1.8/)

Skill response: pass strings with `--arg`, JSON values with `--argjson`, JSON
files with `--slurpfile`, and raw files with `--rawfile` instead of
concatenating user-controlled text into the jq filter.

### Failure mode: replacing a file before validating the result

> "overwrite the current contents of the specified file without warning."
> - [PowerShell about_Redirection](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_redirection)

Skill response: write to a temporary file, validate the saved output, and only
then replace the target. For validation checks, use `jq -e` deliberately and
check the consumer's contract: one JSON value, JSONL, raw text, or only an exit
status.

### Failure mode: installing only `SKILL.md`

> "A skill is a directory with a `SKILL.md` file plus optional scripts and references."
> - [OpenAI Codex Agent Skills docs](https://developers.openai.com/codex/skills)

> "Agents load skills progressively"
> - [Agent Skills specification](https://agentskills.io/specification)

Skill response: install `skills/jq-cli/` as a whole. The main `SKILL.md` stays
short, while `references/execution.md`, `references/quoting.md`, and
`references/gotchas.md` hold detail that agents load only when needed.

## Evaluation Loop

The skill includes a small seed set of evaluation cases in
`skills/jq-cli/evals/evals.json`. These are not OpenAI hosted Evals API objects.

From the repository root, prepare a local workspace outside the repository, then
run each case in a clean agent session with and without the skill:

```bash
python scripts/prepare_eval_workspace.py --out ../jq-cli-eval-workspace/iteration-1
```

The generated task files include absolute paths to the skill under evaluation.
Record the agent output and pass/fail notes in the generated workspace. Keep
generated eval results out of the installable `skills/jq-cli/` directory.

## Repository Layout

```text
README.md
INSTALL.md
scripts/
skills/jq-cli/
```

`skills/jq-cli/` is the single source of truth for the installable Skill.

## Sources And License

This skill is based on official jq, PowerShell, and Agent Skills
documentation:

- https://jqlang.org/manual/v1.8/
- https://jqlang.org/download/
- https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_parsing
- https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_quoting_rules
- https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_redirection
- https://developers.openai.com/codex/skills
- https://code.claude.com/docs/en/skills
- https://cursor.com/docs/skills.md
- https://agentskills.io/specification

This repository is licensed under the MIT License. See [LICENSE](LICENSE).
