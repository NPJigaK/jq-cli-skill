#!/usr/bin/env python3
"""Tests for the local jq-cli eval workspace helper."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from prepare_eval_workspace import prepare_workspace


class PrepareEvalWorkspaceTests(unittest.TestCase):
    def test_agent_task_does_not_include_expected_output_or_assertions(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            skill_path = root / "skill"
            skill_path.mkdir()
            (skill_path / "SKILL.md").write_text(
                "---\nname: jq-cli\ndescription: Test skill.\n---\n\n# jq-cli\n",
                encoding="utf-8",
            )

            evals_path = root / "evals.json"
            evals_path.write_text(
                json.dumps(
                    {
                        "schema_version": 2,
                        "skill_name": "jq-cli",
                        "evals": [
                            {
                                "id": "leak-check",
                                "agent": {
                                    "prompt": "Do the jq task."
                                },
                                "grader": {
                                    "expected_output": "SECRET EXPECTED RUBRIC",
                                    "assertions": ["SECRET ASSERTION"],
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            out_dir = root / "out"
            prepare_workspace(evals_path, skill_path, out_dir)

            task_texts = [
                (out_dir / "leak-check" / mode / "TASK.md").read_text(encoding="utf-8")
                for mode in ("with_skill", "without_skill")
            ]
            public_manifest = (out_dir / "manifest.json").read_text(encoding="utf-8")
            evaluation_path = out_dir / "grading" / "leak-check" / "EVALUATION.md"
            self.assertTrue(evaluation_path.is_file(), "EVALUATION.md should be generated")
            evaluation_text = evaluation_path.read_text(encoding="utf-8")

            for task_text in task_texts:
                self.assertIn("Do the jq task.", task_text)
                self.assertNotIn("SECRET EXPECTED RUBRIC", task_text)
                self.assertNotIn("SECRET ASSERTION", task_text)
            self.assertIn("SECRET EXPECTED RUBRIC", evaluation_text)
            self.assertIn("SECRET ASSERTION", evaluation_text)
            self.assertNotIn("SECRET EXPECTED RUBRIC", public_manifest)
            self.assertNotIn("SECRET ASSERTION", public_manifest)

    def test_nested_agent_grader_schema_generates_public_files_without_grader_leakage(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            skill_path = root / "skill"
            skill_path.mkdir()
            (skill_path / "SKILL.md").write_text(
                "---\nname: jq-cli\ndescription: Test skill.\n---\n\n# jq-cli\n",
                encoding="utf-8",
            )

            evals_path = root / "evals.json"
            evals_path.write_text(
                json.dumps(
                    {
                        "schema_version": 2,
                        "skill_name": "jq-cli",
                        "evals": [
                            {
                                "id": "nested-schema",
                                "metadata": {"tags": ["modules"]},
                                "agent": {
                                    "prompt": "Inspect the jq module tree.",
                                    "public_files": [
                                        {
                                            "path": "transform.jq",
                                            "content": 'include "helpers"; .items',
                                        },
                                        {
                                            "path": "modules/helpers.jq",
                                            "content": "def active: .active == true;",
                                        },
                                        {
                                            "path": "empty.jsonl",
                                            "content": "",
                                        },
                                    ],
                                },
                                "grader": {
                                    "expected_output": "SECRET EXPECTED RUBRIC",
                                    "assertions": ["SECRET ASSERTION"],
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            out_dir = root / "out"
            prepare_workspace(evals_path, skill_path, out_dir)

            task_text = (out_dir / "nested-schema" / "with_skill" / "TASK.md").read_text(
                encoding="utf-8"
            )
            public_manifest = (out_dir / "manifest.json").read_text(encoding="utf-8")
            grading_manifest = (out_dir / "grading" / "manifest.json").read_text(
                encoding="utf-8"
            )

            self.assertIn("Inspect the jq module tree.", task_text)
            self.assertIn("public/transform.jq", task_text)
            self.assertEqual(
                'include "helpers"; .items',
                (out_dir / "nested-schema" / "public" / "transform.jq").read_text(
                    encoding="utf-8"
                ),
            )
            self.assertEqual(
                "def active: .active == true;",
                (out_dir / "nested-schema" / "public" / "modules" / "helpers.jq").read_text(
                    encoding="utf-8"
                ),
            )
            self.assertEqual(
                "",
                (out_dir / "nested-schema" / "public" / "empty.jsonl").read_text(
                    encoding="utf-8"
                ),
            )
            self.assertNotIn("SECRET EXPECTED RUBRIC", task_text)
            self.assertNotIn("SECRET ASSERTION", task_text)
            self.assertNotIn("SECRET EXPECTED RUBRIC", public_manifest)
            self.assertNotIn("SECRET ASSERTION", public_manifest)
            self.assertIn("SECRET EXPECTED RUBRIC", grading_manifest)
            self.assertIn("SECRET ASSERTION", grading_manifest)


if __name__ == "__main__":
    unittest.main()
