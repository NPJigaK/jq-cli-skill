# Install jq-cli Skill

Use this file when you want an agent to install the skill for you without a
plugin marketplace.

## Copy-Paste Agent Prompt

```text
Install the jq-cli Codex skill from this repository.

Repository: https://github.com/NPJigaK/jq-cli-skill
Skill path: skills/jq-cli

Steps:
1. Clone or download the repository to a temporary location.
2. Verify that skills/jq-cli/SKILL.md exists and has valid YAML frontmatter
   with name: jq-cli and a non-empty description.
3. Install the skill directory without modifying its contents:
   - Prefer $HOME/.agents/skills/jq-cli for current Codex setups.
   - If this Codex setup uses CODEX_HOME, use $CODEX_HOME/skills/jq-cli.
   - If this setup uses the older Codex home path, use $HOME/.codex/skills/jq-cli.
4. Do not overwrite an existing jq-cli skill without asking first.
5. After installation, tell me to restart Codex or start a new thread.
```

## Direct Codex Prompt

```text
$skill-installer install https://github.com/NPJigaK/jq-cli-skill/tree/main/skills/jq-cli
```

## Manual Install

From a local checkout of this repository:

```bash
mkdir -p "$HOME/.agents/skills"
cp -R skills/jq-cli "$HOME/.agents/skills/jq-cli"
```

Restart Codex or start a new thread after installing.
