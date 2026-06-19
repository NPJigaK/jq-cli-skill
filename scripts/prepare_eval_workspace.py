#!/usr/bin/env python3
"""Prepare local jq-cli skill evaluation run directories."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


TOP_LEVEL_KEYS = {"schema_version", "skill_name", "metadata", "evals"}
EVAL_KEYS = {"id", "metadata", "agent", "grader"}
AGENT_KEYS = {"prompt", "public_files"}
GRADER_KEYS = {"expected_output", "assertions"}
PUBLIC_FILE_KEYS = {"path", "content"}


def fail(message: str) -> None:
    raise SystemExit(f"error: {message}")


def slug(value: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip()).strip("-._")
    return normalized.lower() or "eval-case"


def require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or value.strip() == "":
        fail(f"{label} must be a non-empty string")
    return value


def require_text(value: Any, label: str) -> str:
    if not isinstance(value, str):
        fail(f"{label} must be a string")
    return value


def normalize_id(value: Any, label: str) -> str:
    if not isinstance(value, (str, int)) or str(value).strip() == "":
        fail(f"{label} must be a non-empty string or integer")
    return str(value)


def require_string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        fail(f"{label} must be an array of strings when present")
    return value


def require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{label} must be an object")
    return value


def normalize_public_files(value: Any, label: str) -> list[dict[str, str]]:
    if not isinstance(value, list):
        fail(f"{label} must be an array of objects when present")

    public_files: list[dict[str, str]] = []
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            fail(f"{label}[{index}] must be an object")
        extra_keys = sorted(set(item) - PUBLIC_FILE_KEYS)
        if extra_keys:
            fail(f"{label}[{index}] has unexpected keys: {', '.join(extra_keys)}")

        missing = sorted(PUBLIC_FILE_KEYS - set(item))
        if missing:
            fail(f"{label}[{index}] is missing required keys: {', '.join(missing)}")

        public_files.append(
            {
                "path": require_string(item["path"], f"{label}[{index}].path"),
                "content": require_text(item["content"], f"{label}[{index}].content"),
            }
        )

    return public_files


def normalize_case(case: dict[str, Any], index: int) -> dict[str, Any]:
    extra_case_keys = sorted(set(case) - EVAL_KEYS)
    if extra_case_keys:
        fail(f"evals[{index}] has unexpected keys: {', '.join(extra_case_keys)}")

    missing = sorted({"id", "agent", "grader"} - set(case))
    if missing:
        fail(f"evals[{index}] is missing required keys: {', '.join(missing)}")

    case_id = normalize_id(case.get("id"), f"evals[{index}].id")
    agent = require_object(case["agent"], f"evals[{index}].agent")
    grader = require_object(case["grader"], f"evals[{index}].grader")
    metadata = case.get("metadata", {})
    if metadata is not None and not isinstance(metadata, dict):
        fail(f"evals[{index}].metadata must be an object when present")

    extra_agent_keys = sorted(set(agent) - AGENT_KEYS)
    if extra_agent_keys:
        fail(f"evals[{index}].agent has unexpected keys: {', '.join(extra_agent_keys)}")
    extra_grader_keys = sorted(set(grader) - GRADER_KEYS)
    if extra_grader_keys:
        fail(f"evals[{index}].grader has unexpected keys: {', '.join(extra_grader_keys)}")

    missing_agent = sorted({"prompt"} - set(agent))
    if missing_agent:
        fail(f"evals[{index}].agent is missing required keys: {', '.join(missing_agent)}")
    missing_grader = sorted({"expected_output"} - set(grader))
    if missing_grader:
        fail(f"evals[{index}].grader is missing required keys: {', '.join(missing_grader)}")

    normalized_agent = {
        "prompt": require_string(agent["prompt"], f"evals[{index}].agent.prompt"),
        "public_files": normalize_public_files(
            agent.get("public_files", []),
            f"evals[{index}].agent.public_files",
        ),
    }
    normalized_grader = {
        "expected_output": require_string(
            grader["expected_output"],
            f"evals[{index}].grader.expected_output",
        ),
    }
    if "assertions" in grader:
        normalized_grader["assertions"] = require_string_list(
            grader["assertions"],
            f"evals[{index}].grader.assertions",
        )

    return {
        "id": case_id,
        "metadata": metadata or {},
        "agent": normalized_agent,
        "grader": normalized_grader,
    }


def load_cases(path: Path) -> tuple[str, list[dict[str, Any]]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{path} is not valid JSON: {exc}")

    if not isinstance(data, dict):
        fail("evals file must be a JSON object")

    extra_top_keys = sorted(set(data) - TOP_LEVEL_KEYS)
    if extra_top_keys:
        fail(f"unexpected top-level keys: {', '.join(extra_top_keys)}")

    skill_name = data.get("skill_name")
    if skill_name != "jq-cli":
        fail("skill_name must be jq-cli")

    schema_version = data.get("schema_version")
    if schema_version != 2:
        fail("schema_version must be 2")

    cases = data.get("evals")
    if not isinstance(cases, list) or not cases:
        fail("evals must be a non-empty array")

    seen_ids: set[str] = set()
    normalized_cases: list[dict[str, Any]] = []
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            fail(f"evals[{index}] must be an object")

        normalized_case = normalize_case(case, index)
        case_id_text = normalized_case["id"]
        if case_id_text in seen_ids:
            fail(f"duplicate eval id: {case_id_text}")
        seen_ids.add(case_id_text)

        normalized_cases.append(normalized_case)

    return skill_name, normalized_cases


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def task_markdown(skill_name: str, skill_path: Path, case: dict[str, Any], mode: str) -> str:
    if mode == "with_skill":
        setup = (
            f"Start a clean agent session with the `{skill_name}` skill installed or "
            f"available from `{skill_path.as_posix()}`. Use the skill for the task."
        )
    else:
        setup = (
            f"Start a clean baseline session where the `{skill_name}` skill is not "
            "installed or enabled. If comparing a revision, use the previous skill "
            "snapshot instead."
        )

    agent = case["agent"]
    files = [f"public/{item['path']}" for item in agent["public_files"]]
    file_block = "\n".join(f"- `{item}`" for item in files) if files else "- None"
    return f"""# {case["id"]} ({mode})

{setup}

## Task

{agent["prompt"]}

## Input Files

{file_block}

## Record

- Save the agent response or produced artifacts in this directory.
- Note any safety, quoting, output-contract, or resource-use issues.
"""


def evaluation_markdown(case: dict[str, Any]) -> str:
    grader = case["grader"]
    assertions = grader.get("assertions", [])
    assertions_block = ""
    if assertions:
        assertion_lines = "\n".join(f"- {item}" for item in assertions)
        assertions_block = f"""
## Assertions

{assertion_lines}
"""

    return f"""# {case["id"]} Evaluation

Do not pass this file to the agent under evaluation. Use it only after the
agent response is recorded.

## Expected Output

{grader["expected_output"]}
{assertions_block}

## Record

- Record whether the expected output was satisfied for each mode.
- Note any safety, quoting, output-contract, or resource-use issues.
"""


def workspace_readme(skill_name: str, cases: list[dict[str, Any]]) -> str:
    case_lines = "\n".join(f"- `{case['id']}`" for case in cases)
    return f"""# jq-cli Eval Workspace

Run each case in a fresh context. Give the agent only the case's agent-visible
bundle: the mode-specific `TASK.md` plus any files under that case's `public/`
directory. Compare `with_skill` against `without_skill` or against an older
skill snapshot after the response is recorded. Keep generated outputs in this
workspace, not in the skill directory.

Use each case's `grading/<case-id>/EVALUATION.md` for human grading only. Do not
include the `grading/` directory in the agent prompt or workspace.

Skill: `{skill_name}`

Cases:
{case_lines}
"""


def public_manifest_case(case: dict[str, Any]) -> dict[str, Any]:
    agent = case["agent"]
    return {
        "id": case["id"],
        "metadata": case["metadata"],
        "agent": {
            "prompt": agent["prompt"],
            "public_files": [item["path"] for item in agent["public_files"]],
        },
    }


def safe_public_path(public_root: Path, relative_path: str) -> Path:
    target = (public_root / relative_path).resolve()
    public_root = public_root.resolve()
    if target == public_root or not target.is_relative_to(public_root):
        fail(f"public file path escapes case public directory: {relative_path}")
    return target


def write_public_files(case_dir: Path, case: dict[str, Any]) -> None:
    public_root = case_dir / "public"
    for public_file in case["agent"]["public_files"]:
        write_text(
            safe_public_path(public_root, public_file["path"]),
            public_file["content"],
        )


def prepare_workspace(evals_path: Path, skill_path: Path, out_dir: Path) -> None:
    evals_path = evals_path.resolve()
    skill_path = skill_path.resolve()
    out_dir = out_dir.resolve()

    if not evals_path.is_file():
        fail(f"evals file does not exist: {evals_path}")
    if not (skill_path / "SKILL.md").is_file():
        fail(f"skill path must contain SKILL.md: {skill_path}")

    skill_name, cases = load_cases(evals_path)

    if out_dir.exists() and any(out_dir.iterdir()):
        fail(f"output directory already exists and is not empty: {out_dir}")
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "skill_name": skill_name,
        "evals_path": evals_path.as_posix(),
        "skill_path": skill_path.as_posix(),
        "case_count": len(cases),
        "cases": [public_manifest_case(case) for case in cases],
    }
    write_text(out_dir / "manifest.json", json.dumps(manifest, indent=2) + "\n")
    grading_manifest = {
        "skill_name": skill_name,
        "evals_path": evals_path.as_posix(),
        "skill_path": skill_path.as_posix(),
        "case_count": len(cases),
        "cases": cases,
    }
    write_text(
        out_dir / "grading" / "manifest.json",
        json.dumps(grading_manifest, indent=2) + "\n",
    )
    write_text(out_dir / "README.md", workspace_readme(skill_name, cases))

    used_slugs: set[str] = set()
    for case in cases:
        case_slug = slug(case["id"])
        if case_slug in used_slugs:
            fail(f"eval id produces duplicate directory name: {case['id']}")
        used_slugs.add(case_slug)

        case_dir = out_dir / case_slug
        write_text(out_dir / "grading" / case_slug / "EVALUATION.md", evaluation_markdown(case))
        write_public_files(case_dir, case)

        for mode in ("with_skill", "without_skill"):
            write_text(
                case_dir / mode / "TASK.md",
                task_markdown(skill_name, skill_path, case, mode),
            )

    print(f"Prepared {len(cases)} eval cases in {out_dir}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Create local with-skill and baseline task directories from jq-cli evals.json."
    )
    parser.add_argument(
        "--evals",
        type=Path,
        default=Path("skills/jq-cli/evals/evals.json"),
        help="Path to evals.json.",
    )
    parser.add_argument(
        "--skill-path",
        type=Path,
        default=Path("skills/jq-cli"),
        help="Path to the skill under evaluation.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Empty output directory for the prepared eval workspace.",
    )
    args = parser.parse_args(argv)

    prepare_workspace(args.evals, args.skill_path, args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
