# jq CLI Agent Skill

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Latest release](https://img.shields.io/github/v/release/NPJigaK/jq-cli-skill?label=release)](https://github.com/NPJigaK/jq-cli-skill/releases/latest)

A portable Agent Skill for using the `jq` command-line JSON processor safely
and reliably from Codex, Claude Code, Cursor, and other SKILL.md-compatible
coding agents.

## Quick Start

```bash
npx skills add NPJigaK/jq-cli-skill --skill jq-cli --agent codex
```

```text
$jq-cli Inspect this JSON file and summarize the top-level shape.
```

Works with Codex, Claude Code, Cursor, and other Agent Skills clients.

The installable Skill is:

```text
skills/jq-cli/
```

Install that directory as a whole. Do not install the repository root as a
Skill, and do not copy only `SKILL.md`; the `references/` directory is part of
the runtime guidance.

## Install Options

### Codex

```text
Use $skill-installer to install the jq-cli skill from:

https://github.com/NPJigaK/jq-cli-skill/tree/main/skills/jq-cli

Install it for my user account. Inspect the skill contents before installing it,
and do not modify the source repository.
```

```bash
npx skills add NPJigaK/jq-cli-skill --skill jq-cli --agent codex
```

Invoke with:

```text
$jq-cli Inspect this JSON file and summarize the top-level shape.
```

### Claude Code

```bash
npx skills add NPJigaK/jq-cli-skill --skill jq-cli --agent claude-code
```

Invoke with the client-supported skill command or skill menu, for example:

```text
/jq-cli Validate this JSONL file without loading the whole file into memory.
```

### Cursor

```bash
npx skills add NPJigaK/jq-cli-skill --skill jq-cli --agent cursor
```

Invoke with the client-supported skill command or skill menu, for example:

```text
/jq-cli Filter these records by a user-provided status value.
```

### Agent Skills CLI

```bash
npx skills add NPJigaK/jq-cli-skill --skill jq-cli
```

Use without installing:

```bash
npx skills use NPJigaK/jq-cli-skill@jq-cli
```

More install options are in [INSTALL.md](INSTALL.md).

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
- avoiding implicit jq module search paths for untrusted filters
- handling native Windows `jq.exe` newline translation in WSL/MSYS2/Cygwin
- distinguishing JSONL from JSON Text Sequences and streaming parse diagnostics

## Evaluation Loop

The skill includes a small seed set of evaluation cases in
`skills/jq-cli/evals/evals.json`. These are not OpenAI hosted Evals API objects.
When adding runtime guidance, add or update an eval case unless the change is
pure wording with no observable behavior.

Eval cases use a split schema: `agent` contains only the prompt and public
fixtures that may be shown to the agent; `grader` contains expected output and
assertions that must stay hidden until after the response is recorded.

From the repository root, prepare a local workspace outside the repository, then
run each case in a clean agent session with and without the skill:

```bash
python scripts/prepare_eval_workspace.py --out ../jq-cli-eval-workspace/iteration-1
```

Give the agent only the case's agent-visible bundle: the mode-specific
`TASK.md` plus any files under that case's `public/` directory. Use
`grading/<case-id>/EVALUATION.md` only after the response is recorded; it
contains the expected output and assertions. Keep generated eval results out of
the installable `skills/jq-cli/` directory.

## Repository Layout

```text
README.md
INSTALL.md
scripts/
skills/jq-cli/
```

`skills/jq-cli/` is the single source of truth for the installable Skill.

## Sources And License

This skill is based on the official jq 1.8 manual and Agent Skills
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
