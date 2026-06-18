# Installation

The installable Skill directory is:

```text
skills/jq-cli/
```

Install that directory as a whole. Do not install the repository root as a
Skill, and do not copy only `SKILL.md`; the `references/` directory is part of
the runtime guidance.

The same Skill directory is installed for every Agent Skills client. Only the
install path and invocation syntax vary by client.

## Install Options

### Codex

Use Codex's skill installer:

```text
Use $skill-installer to install the jq-cli skill from:

https://github.com/NPJigaK/jq-cli-skill/tree/main/skills/jq-cli

Install it for my user account. Inspect the skill contents before installing it,
and do not modify the source repository.
```

Project-scoped install:

```text
.agents/skills/jq-cli/
```

User/global install:

```text
$HOME/.agents/skills/jq-cli/
```

Older or custom Codex setups may use:

```text
$CODEX_HOME/skills/jq-cli/
$HOME/.codex/skills/jq-cli/
```

CLI install:

```bash
npx skills add NPJigaK/jq-cli-skill --skill jq-cli --agent codex
```

CLI user/global install:

```bash
npx skills add NPJigaK/jq-cli-skill --skill jq-cli --agent codex --global
```

Invoke:

```text
$jq-cli Inspect this JSON file and summarize the top-level shape.
```

Use without installing:

```bash
npx skills use NPJigaK/jq-cli-skill@jq-cli --agent codex
```

### Claude Code

Project-scoped install:

```text
.claude/skills/jq-cli/
```

User/global install:

```text
~/.claude/skills/jq-cli/
```

CLI install:

```bash
npx skills add NPJigaK/jq-cli-skill --skill jq-cli --agent claude-code
```

CLI user/global install:

```bash
npx skills add NPJigaK/jq-cli-skill --skill jq-cli --agent claude-code --global
```

Invoke with the client-supported skill command or skill menu, for example:

```text
/jq-cli Validate this JSONL file without loading the whole file into memory.
```

Use without installing:

```bash
npx skills use NPJigaK/jq-cli-skill@jq-cli --agent claude-code
```

### Cursor

Project-scoped install:

```text
.cursor/skills/jq-cli/
```

User/global install:

```text
~/.cursor/skills/jq-cli/
```

CLI install:

```bash
npx skills add NPJigaK/jq-cli-skill --skill jq-cli --agent cursor
```

CLI user/global install:

```bash
npx skills add NPJigaK/jq-cli-skill --skill jq-cli --agent cursor --global
```

Invoke with the client-supported skill command or skill menu, for example:

```text
/jq-cli Filter these records by a user-provided status value.
```

Use without installing:

```bash
npx skills use NPJigaK/jq-cli-skill@jq-cli --agent cursor
```

### Shared `.agents` Layout

Some Agent Skills clients also load the shared project-scoped path:

```text
.agents/skills/jq-cli/
```

or user/global path:

```text
~/.agents/skills/jq-cli/
```

### Agent Skills CLI

```bash
npx skills add NPJigaK/jq-cli-skill --skill jq-cli
```

Use without installing:

```bash
npx skills use NPJigaK/jq-cli-skill@jq-cli
```

## Copy-Paste Agent Prompt

Use this prompt when you want an agent to install the skill without relying on a
marketplace or CLI:

```text
Install the jq-cli Agent Skill from this repository for the target agent I am
using.

Repository: https://github.com/NPJigaK/jq-cli-skill
Skill path: skills/jq-cli

Steps:
1. Clone or download the repository to a temporary location.
2. Verify that skills/jq-cli/SKILL.md exists and has valid YAML frontmatter
   with name: jq-cli and a non-empty description.
3. Install the whole skills/jq-cli directory without modifying its contents.
   Do not install the repository root, and do not copy only SKILL.md.
4. Choose exactly one destination unless I ask for multiple agents:
   - Codex project: .agents/skills/jq-cli in the project root.
   - Codex global: prefer $HOME/.agents/skills/jq-cli.
   - Codex with CODEX_HOME: use $CODEX_HOME/skills/jq-cli.
   - Older Codex setups: use $HOME/.codex/skills/jq-cli.
   - Claude Code project: use .claude/skills/jq-cli in the project root.
   - Claude Code global: use $HOME/.claude/skills/jq-cli.
   - Cursor project: use .cursor/skills/jq-cli for Cursor-only scope, or
     .agents/skills/jq-cli for portable project scope.
   - Cursor global: use $HOME/.cursor/skills/jq-cli for Cursor-only scope, or
     $HOME/.agents/skills/jq-cli for portable global scope.
   - Generic SKILL.md-compatible agent: ask for its supported skill directory
     if it is not obvious.
5. Do not overwrite an existing jq-cli skill without asking first.
6. After installation, tell me how to reload the target agent:
   - Codex: restart Codex or start a new thread if the skill does not appear.
   - Claude Code: restart only if the top-level skills directory did not
     exist when the session started.
   - Cursor: restart Cursor or reopen the project.
```

## Notes

- The Skill content is the same across Codex, Claude Code, Cursor, and other
  SKILL.md-compatible clients.
- `references/` contains runtime guidance that the skill loads when needed.
- `agents/openai.yaml` is OpenAI/Codex UI metadata. Clients that do not read it
  can ignore it without changing the Skill semantics.
- `evals/` contains portable repository validation cases. They are not OpenAI
  Evals API objects; runner-specific configs should be generated from them when
  needed. Ordinary clients can ignore this directory.
- Invocation syntax is client-specific: Codex uses `$jq-cli`; Claude Code and
  Cursor commonly use `/jq-cli` or a skill menu.
