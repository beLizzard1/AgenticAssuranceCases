from __future__ import annotations

from copy import deepcopy
from typing import Any


BOOTSTRAP_PATTERNS: dict[str, dict[str, Any]] = {
    "generic": {
        "description": "General-purpose bootstrap scaffold for a new assurance case.",
        "root": {
            "node_type": "claim",
            "title": "{system_name} is ready for assurance review",
            "annotation": "Initial bootstrap claim for {system_name}. {system_context}",
            "children": [
                {
                    "node_type": "argument",
                    "link_type": "supports",
                    "title": "Selected assurance strategy",
                    "annotation": "Initial strategy: {strategy}",
                    "attributes": {"bootstrap-role": "strategy"},
                },
                {
                    "node_type": "comment",
                    "link_type": "commentson",
                    "title": "Operational context",
                    "annotation": "{system_context}",
                    "attributes": {"bootstrap-role": "context"},
                },
                {
                    "node_type": "comment",
                    "link_type": "commentson",
                    "title": "Assumptions",
                    "annotation": "Bootstrap assumptions that must be checked during refinement.",
                    "attributes": {"bootstrap-role": "assumption"},
                },
                {
                    "node_type": "evidence",
                    "link_type": "isevidencefor",
                    "title": "Evidence placeholders",
                    "annotation": "Known evidence needs and open gaps.",
                    "attributes": {"bootstrap-role": "evidence-placeholder", "bootstrap-placeholder": "true"},
                },
                {
                    "node_type": "defeater",
                    "link_type": "defeats",
                    "title": "Open challenge",
                    "annotation": "Potential weakness, mismatch, or unresolved uncertainty.",
                    "attributes": {"bootstrap-role": "defeater"},
                },
            ],
        },
    },
    "security": {
        "description": "Bootstrap scaffold oriented around security assurance.",
        "root": {
            "node_type": "claim",
            "title": "{system_name} security posture is ready for assurance review",
            "annotation": "Security-oriented bootstrap claim for {system_name}. {system_context}",
            "children": [
                {
                    "node_type": "argument",
                    "link_type": "supports",
                    "title": "Security strategy",
                    "annotation": "Initial strategy: {strategy}",
                    "attributes": {"bootstrap-role": "strategy"},
                },
                {
                    "node_type": "comment",
                    "link_type": "commentson",
                    "title": "Threat context",
                    "annotation": "{system_context}",
                    "attributes": {"bootstrap-role": "context"},
                },
                {
                    "node_type": "evidence",
                    "link_type": "isevidencefor",
                    "title": "Security evidence gaps",
                    "annotation": "Evidence still required to justify the security claim.",
                    "attributes": {"bootstrap-role": "evidence-placeholder", "bootstrap-placeholder": "true"},
                },
                {
                    "node_type": "defeater",
                    "link_type": "defeats",
                    "title": "Security challenge",
                    "annotation": "Potential security assumption or threat mismatch.",
                    "attributes": {"bootstrap-role": "defeater"},
                },
            ],
        },
    },
    "safety": {
        "description": "Bootstrap scaffold oriented around safety assurance.",
        "root": {
            "node_type": "claim",
            "title": "{system_name} safety posture is ready for assurance review",
            "annotation": "Safety-oriented bootstrap claim for {system_name}. {system_context}",
            "children": [
                {
                    "node_type": "argument",
                    "link_type": "supports",
                    "title": "Safety strategy",
                    "annotation": "Initial strategy: {strategy}",
                    "attributes": {"bootstrap-role": "strategy"},
                },
                {
                    "node_type": "comment",
                    "link_type": "commentson",
                    "title": "Operating context",
                    "annotation": "{system_context}",
                    "attributes": {"bootstrap-role": "context"},
                },
                {
                    "node_type": "evidence",
                    "link_type": "isevidencefor",
                    "title": "Safety evidence gaps",
                    "annotation": "Evidence still required to justify the safety claim.",
                    "attributes": {"bootstrap-role": "evidence-placeholder", "bootstrap-placeholder": "true"},
                },
                {
                    "node_type": "defeater",
                    "link_type": "defeats",
                    "title": "Safety challenge",
                    "annotation": "Potential hazard assumption or operating-environment mismatch.",
                    "attributes": {"bootstrap-role": "defeater"},
                },
            ],
        },
    },
}


def list_bootstrap_patterns() -> list[dict[str, str]]:
    return [
        {"name": name, "description": pattern["description"]}
        for name, pattern in sorted(BOOTSTRAP_PATTERNS.items())
    ]


def get_bootstrap_pattern(name: str) -> dict[str, Any]:
    pattern = BOOTSTRAP_PATTERNS.get(name)
    if pattern is None:
        raise KeyError(f"Unknown bootstrap pattern: {name}")
    return deepcopy(pattern)


def render_bootstrap_pattern(
    name: str,
    *,
    system_name: str = "the system",
    system_context: str = "No system context provided.",
    strategy: str = "hybrid",
) -> dict[str, Any]:
    pattern = get_bootstrap_pattern(name)

    def render(value: Any) -> Any:
        if isinstance(value, str):
            return value.format(system_name=system_name, system_context=system_context, strategy=strategy)
        if isinstance(value, list):
            return [render(item) for item in value]
        if isinstance(value, dict):
            return {key: render(item) for key, item in value.items()}
        return value

    return render(pattern)
