# jq CLI Agent Skill

Agent Skill for using the `jq` command-line JSON processor safely and
reliably from Codex, Claude Code, Cursor, and other SKILL.md-compatible coding
agents.

The canonical skill lives at:

```text
skills/jq-cli/
```

Keep `skills/jq-cli/` as the single source of truth. Install it by copying or
symlinking that folder into the skill directory used by your agent.

It focuses on the parts agents often get wrong:

- shell quoting across POSIX shells, PowerShell, and cmd.exe
- passing user values with `--arg`, `--argjson`, `--slurpfile`, and `--rawfile`
- avoiding accidental in-place truncation
- choosing safe input modes for JSON, JSONL, raw text, and large files
- interpreting `jq -e` exit statuses for validation checks
- avoiding module/import and precision surprises

## Agent Install Prompt

If a user wants an agent to install it without relying on a marketplace, paste
the prompt from [INSTALL.md](INSTALL.md).

## Codex

```text
$skill-installer install https://github.com/NPJigaK/jq-cli-skill/tree/main/skills/jq-cli
```

Manual global install:

```bash
mkdir -p "$HOME/.agents/skills"
cp -R skills/jq-cli "$HOME/.agents/skills/jq-cli"
```

For older or custom Codex setups, `$CODEX_HOME/skills` or
`$HOME/.codex/skills` may be used instead. Restart Codex after installing.

## Claude Code

Global install:

```bash
mkdir -p "$HOME/.claude/skills"
cp -R skills/jq-cli "$HOME/.claude/skills/jq-cli"
```

Project install:

```bash
mkdir -p .claude/skills
cp -R skills/jq-cli .claude/skills/jq-cli
```

Claude Code normally watches existing skill directories, but restart Claude
Code if the top-level skills directory did not exist when the session started.

## Cursor

Portable global install, shared with agents that read `.agents/skills`:

```bash
mkdir -p "$HOME/.agents/skills"
cp -R skills/jq-cli "$HOME/.agents/skills/jq-cli"
```

Cursor-only global install:

```bash
mkdir -p "$HOME/.cursor/skills"
cp -R skills/jq-cli "$HOME/.cursor/skills/jq-cli"
```

Project install:

```bash
mkdir -p .agents/skills
cp -R skills/jq-cli .agents/skills/jq-cli
```

Cursor also supports `.cursor/skills/` for project-local Cursor-only skills.
Restart Cursor or reopen the project after installing.

## Sources

This skill is based on the official jq 1.8 manual and Agent Skills
documentation:

- https://jqlang.org/manual/v1.8/
- https://jqlang.org/download/
- https://developers.openai.com/codex/skills
- https://code.claude.com/docs/en/skills
- https://cursor.com/docs/skills.md
- https://agentskills.io/specification

No repository license is declared yet. Choose and add a license before public
redistribution if you want others to reuse the contents under explicit terms.
