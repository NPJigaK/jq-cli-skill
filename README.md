# jq CLI Skill

Agent Skill for using the `jq` command-line JSON processor safely and
reliably from Codex and other SKILL.md-compatible coding agents.

The skill lives at:

```text
skills/jq-cli/
```

It focuses on the parts agents often get wrong:

- shell quoting across POSIX shells, PowerShell, and cmd.exe
- passing user values with `--arg`, `--argjson`, `--slurpfile`, and `--rawfile`
- avoiding accidental in-place truncation
- choosing safe input modes for JSON, JSONL, raw text, and large files
- interpreting `jq -e` exit statuses for validation checks
- avoiding module/import and precision surprises

## Install With Codex

Inside Codex, paste this:

```text
$skill-installer install https://github.com/NPJigaK/jq-cli-skill/tree/main/skills/jq-cli
```

Restart Codex or start a new thread after installation.

## Agent Install Prompt

If a user wants an agent to install it without relying on a marketplace, paste
the prompt from [INSTALL.md](INSTALL.md).

## Manual Install

Copy or symlink `skills/jq-cli` into one of Codex's skill locations:

```bash
mkdir -p "$HOME/.agents/skills"
cp -R skills/jq-cli "$HOME/.agents/skills/jq-cli"
```

For older or custom Codex setups, `$CODEX_HOME/skills` or
`$HOME/.codex/skills` may be used instead. Restart Codex after installing.

## Sources

This skill is based on the official jq 1.8 manual and OpenAI Codex Agent Skills
documentation:

- https://jqlang.org/manual/v1.8/
- https://jqlang.org/download/
- https://developers.openai.com/codex/skills
- https://agentskills.io/specification

No repository license is declared yet. Choose and add a license before public
redistribution if you want others to reuse the contents under explicit terms.
