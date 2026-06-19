# jq CLI Agent Skill

A portable Agent Skill for using the `jq` command-line JSON processor safely
and reliably from Codex, Claude Code, Cursor, and other SKILL.md-compatible
coding agents.

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

This skill is based on the official jq 1.8 manual and Agent Skills
documentation:

- https://jqlang.org/manual/v1.8/
- https://jqlang.org/download/
- https://developers.openai.com/codex/skills
- https://code.claude.com/docs/en/skills
- https://cursor.com/docs/skills.md
- https://agentskills.io/specification

This repository is licensed under the MIT License. See [LICENSE](LICENSE).
