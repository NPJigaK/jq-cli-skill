# Install jq-cli Agent Skill

Use this file when you want an agent to install the skill for you without a
plugin marketplace.

## Copy-Paste Agent Prompt

```text
Install the jq-cli Agent Skill from this repository for the target agent I am
using.

Repository: https://github.com/NPJigaK/jq-cli-skill
Skill path: skills/jq-cli

Steps:
1. Clone or download the repository to a temporary location.
2. Verify that skills/jq-cli/SKILL.md exists and has valid YAML frontmatter
   with name: jq-cli and a non-empty description.
3. Install the skill directory without modifying its contents. Choose exactly
   one destination unless I ask for multiple agents:
   - Codex global: prefer $HOME/.agents/skills/jq-cli.
   - Codex with CODEX_HOME: use $CODEX_HOME/skills/jq-cli.
   - Older Codex setups: use $HOME/.codex/skills/jq-cli.
   - Claude Code global: use $HOME/.claude/skills/jq-cli.
   - Claude Code project: use .claude/skills/jq-cli in the project root.
   - Cursor portable global: use $HOME/.agents/skills/jq-cli.
   - Cursor-only global: use $HOME/.cursor/skills/jq-cli.
   - Cursor project: prefer .agents/skills/jq-cli, or .cursor/skills/jq-cli
     if the user wants Cursor-only project scope.
   - Generic SKILL.md-compatible agent: ask for its supported skill directory
     if it is not obvious.
4. Do not overwrite an existing jq-cli skill without asking first.
5. After installation, tell me how to reload the target agent:
   - Codex: restart Codex or start a new thread.
   - Claude Code: restart only if the top-level skills directory did not
     exist when the session started.
   - Cursor: restart Cursor or reopen the project.
```

## Direct Codex Prompt

```text
$skill-installer install https://github.com/NPJigaK/jq-cli-skill/tree/main/skills/jq-cli
```

## Manual Installs

From a local checkout of this repository:

Codex or portable Cursor/global Agent Skills:

```bash
mkdir -p "$HOME/.agents/skills"
cp -R skills/jq-cli "$HOME/.agents/skills/jq-cli"
```

Claude Code global:

```bash
mkdir -p "$HOME/.claude/skills"
cp -R skills/jq-cli "$HOME/.claude/skills/jq-cli"
```

Cursor-only global:

```bash
mkdir -p "$HOME/.cursor/skills"
cp -R skills/jq-cli "$HOME/.cursor/skills/jq-cli"
```

Project-local portable install:

```bash
mkdir -p .agents/skills
cp -R skills/jq-cli .agents/skills/jq-cli
```
