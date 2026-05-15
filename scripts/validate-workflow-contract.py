#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Rule:
    name: str
    required_any: tuple[str, ...] = ()
    required_all: tuple[str, ...] = ()
    forbidden: tuple[str, ...] = ()


FILES: tuple[Path, ...] = (
    ROOT / ".opencode/commands/opsx-apply.md",
    ROOT / ".opencode/commands/opsx-archive.md",
    ROOT / ".opencode/skills/openspec-apply-change/SKILL.md",
    ROOT / ".opencode/skills/openspec-archive-change/SKILL.md",
    ROOT / "extern/MITREThreatGraph/.pi/prompts/opsx-apply.md",
    ROOT / "extern/MITREThreatGraph/.pi/prompts/opsx-archive.md",
    ROOT / "extern/MITREThreatGraph/.pi/skills/openspec-apply-change/SKILL.md",
    ROOT / "extern/MITREThreatGraph/.pi/skills/openspec-archive-change/SKILL.md",
    ROOT / ".github/workflows/branch-shared-validation.yml",
    ROOT / ".github/workflows/main-branch-validation.yml",
)


RULES: dict[Path, tuple[Rule, ...]] = {
    ROOT / ".opencode/commands/opsx-apply.md": (
        Rule(
            name="shared branch lifecycle",
            required_all=(
                "Create and switch to a feature branch",
                "Keep the change work on that same branch until archive completes",
                "dirty or branch creation fails",
            ),
            forbidden=("split-opencode-pidev-branches", "pidev", "separate branches"),
        ),
        Rule(name="branch state reporting", required_any=("Active branch or branch transition state",)),
    ),
    ROOT / ".opencode/commands/opsx-archive.md": (
        Rule(
            name="shared archive transition",
            required_all=(
                "Finalize the branch transition",
                "Confirm the active branch matches the change branch",
                "Keep the completed change branch available locally unless the user explicitly asks to delete it",
            ),
            forbidden=("split-opencode-pidev-branches", "pidev", "separate branches"),
        ),
        Rule(name="branch retention", required_any=("Branch retention status", "retained locally for manual cleanup")),
    ),
    ROOT / ".opencode/skills/openspec-apply-change/SKILL.md": (
        Rule(
            name="shared branch lifecycle",
            required_all=(
                "Create and switch to a feature branch",
                "Keep the change work on that same branch until archive completes",
                "branch creation fails",
            ),
            forbidden=("split-opencode-pidev-branches", "pidev", "separate branches"),
        ),
    ),
    ROOT / ".opencode/skills/openspec-archive-change/SKILL.md": (
        Rule(
            name="shared archive transition",
            required_all=(
                "Finalize the branch transition",
                "Confirm the active branch matches the change branch",
                "Keep the completed change branch available locally unless the user explicitly asks to delete it",
            ),
            forbidden=("split-opencode-pidev-branches", "pidev", "separate branches"),
        ),
    ),
    ROOT / "extern/MITREThreatGraph/.pi/prompts/opsx-apply.md": (
        Rule(
            name="shared branch lifecycle",
            required_all=(
                "Create and switch to a feature branch",
                "Keep the change work on that same branch until archive completes",
                "dirty or branch creation fails",
            ),
            forbidden=("split-opencode-pidev-branches", "pidev", "separate branches"),
        ),
        Rule(name="branch state reporting", required_any=("Active branch or branch transition state",)),
    ),
    ROOT / "extern/MITREThreatGraph/.pi/prompts/opsx-archive.md": (
        Rule(
            name="shared archive transition",
            required_all=(
                "Finalize the branch transition",
                "Confirm the active branch matches the change branch",
                "Keep the completed change branch available locally unless the user explicitly asks to delete it",
            ),
            forbidden=("split-opencode-pidev-branches", "pidev", "separate branches"),
        ),
        Rule(name="branch retention", required_any=("Branch retention status", "retained locally for manual cleanup")),
    ),
    ROOT / "extern/MITREThreatGraph/.pi/skills/openspec-apply-change/SKILL.md": (
        Rule(
            name="shared branch lifecycle",
            required_all=(
                "Create and switch to a feature branch",
                "Keep the change work on that same branch until archive completes",
                "branch creation fails",
            ),
            forbidden=("split-opencode-pidev-branches", "pidev", "separate branches"),
        ),
    ),
    ROOT / "extern/MITREThreatGraph/.pi/skills/openspec-archive-change/SKILL.md": (
        Rule(
            name="shared archive transition",
            required_all=(
                "Finalize the branch transition",
                "Confirm the active branch matches the change branch",
                "Keep the completed change branch available locally unless the user explicitly asks to delete it",
            ),
            forbidden=("split-opencode-pidev-branches", "pidev", "separate branches"),
        ),
    ),
    ROOT / ".github/workflows/branch-shared-validation.yml": (
        Rule(
            name="shared validator invocation",
            required_all=("validate-workflow-contract.py",),
            forbidden=("split-opencode-pidev-branches", "trigger_sync_on_nonpackaging", "grep -Fq"),
        ),
    ),
    ROOT / ".github/workflows/main-branch-validation.yml": (
        Rule(
            name="shared validator invocation",
            required_all=("validate-workflow-contract.py",),
            forbidden=("split-opencode-pidev-branches", "trigger_sync_on_nonpackaging", "grep -Fq"),
        ),
    ),
}


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(path)
    return path.read_text(encoding="utf-8")


def validate_file(path: Path) -> list[str]:
    text = read_text(path)
    errors: list[str] = []
    for rule in RULES.get(path, ()): 
        missing = [needle for needle in rule.required_all if needle not in text]
        if missing:
            errors.append(f"{path.relative_to(ROOT)} :: {rule.name} missing required text: {', '.join(missing)}")
        if rule.required_any and not any(needle in text for needle in rule.required_any):
            errors.append(
                f"{path.relative_to(ROOT)} :: {rule.name} missing any of: {', '.join(rule.required_any)}"
            )
        forbidden = [needle for needle in rule.forbidden if needle in text]
        if forbidden:
            errors.append(f"{path.relative_to(ROOT)} :: {rule.name} contains forbidden text: {', '.join(forbidden)}")
    return errors


def main() -> int:
    failures: list[str] = []
    for path in FILES:
        if path not in RULES:
            continue
        try:
            failures.extend(validate_file(path))
        except FileNotFoundError:
            failures.append(f"Missing file: {path.relative_to(ROOT)}")

    if failures:
        print("Workflow contract validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Workflow contract validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
