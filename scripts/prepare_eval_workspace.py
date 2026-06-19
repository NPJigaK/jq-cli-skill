#!/usr/bin/env python3
"""Prepare local jq-cli skill evaluation run directories."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


TOP_LEVEL_KEYS = {"skill_name", "evals"}
EVAL_KEYS = {"id", "prompt", "expected_output", "files"}


def fail(message: str) -> None:
    raise SystemExit(f"error: {message}")


def slug(value: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip()).strip("-._")
    return normalized.lower() or "eval-case"


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

    cases = data.get("evals")
    if not isinstance(cases, list) or not cases:
        fail("evals must be a non-empty array")

    seen_ids: set[str] = set()
    normalized_cases: list[dict[str, Any]] = []
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            fail(f"evals[{index}] must be an object")

        extra_case_keys = sorted(set(case) - EVAL_KEYS)
        if extra_case_keys:
            fail(f"evals[{index}] has unexpected keys: {', '.join(extra_case_keys)}")

        missing = sorted({"id", "prompt", "expected_output"} - set(case))
        if missing:
            fail(f"evals[{index}] is missing required keys: {', '.join(missing)}")

        case_id = case["id"]
        if not isinstance(case_id, (str, int)) or str(case_id).strip() == "":
            fail(f"evals[{index}].id must be a non-empty string or integer")

        case_id_text = str(case_id)
        if case_id_text in seen_ids:
            fail(f"duplicate eval id: {case_id_text}")
        seen_ids.add(case_id_text)

        prompt = case["prompt"]
        expected_output = case["expected_output"]
        if not isinstance(prompt, str) or prompt.strip() == "":
            fail(f"evals[{index}].prompt must be a non-empty string")
        if not isinstance(expected_output, str) or expected_output.strip() == "":
            fail(f"evals[{index}].expected_output must be a non-empty string")

        files = case.get("files", [])
        if not isinstance(files, list) or any(not isinstance(item, str) for item in files):
            fail(f"evals[{index}].files must be an array of strings when present")

        normalized_cases.append(
            {
                "id": case_id_text,
                "prompt": prompt,
                "expected_output": expected_output,
                "files": files,
            }
        )

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

    files = case["files"]
    file_block = "\n".join(f"- `{item}`" for item in files) if files else "- None"

    return f"""# {case["id"]} ({mode})

{setup}

## Task

{case["prompt"]}

## Input Files

{file_block}

## Expected Output

{case["expected_output"]}

## Record

- Save the agent response or produced artifacts in this directory.
- Record whether the expected output was satisfied.
- Note any safety, quoting, output-contract, or resource-use issues.
"""


def workspace_readme(skill_name: str, cases: list[dict[str, Any]]) -> str:
    case_lines = "\n".join(f"- `{case['id']}`" for case in cases)
    return f"""# jq-cli Eval Workspace

Run each case in a fresh context. Compare `with_skill` against `without_skill`
or against an older skill snapshot. Keep generated outputs in this workspace,
not in the skill directory.

Skill: `{skill_name}`

Cases:
{case_lines}
"""


def prepare_workspace(evals_path: Path, skill_path: Path, out_dir: Path) -> None:
    skill_name, cases = load_cases(evals_path)

    if out_dir.exists() and any(out_dir.iterdir()):
        fail(f"output directory already exists and is not empty: {out_dir}")
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "skill_name": skill_name,
        "evals_path": evals_path.as_posix(),
        "skill_path": skill_path.as_posix(),
        "case_count": len(cases),
        "cases": cases,
    }
    write_text(out_dir / "manifest.json", json.dumps(manifest, indent=2) + "\n")
    write_text(out_dir / "README.md", workspace_readme(skill_name, cases))

    used_slugs: set[str] = set()
    for case in cases:
        case_slug = slug(case["id"])
        if case_slug in used_slugs:
            fail(f"eval id produces duplicate directory name: {case['id']}")
        used_slugs.add(case_slug)

        for mode in ("with_skill", "without_skill"):
            write_text(
                out_dir / case_slug / mode / "TASK.md",
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
