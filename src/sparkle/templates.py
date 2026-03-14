from __future__ import annotations

from dataclasses import dataclass

from .models import Node


@dataclass(frozen=True)
class BranchTemplate:
    name: str
    node_type: str
    relation: str
    default_status: str
    description: str
    prompt_prefix: str
    edge_note: str


BRANCH_TEMPLATES: dict[str, BranchTemplate] = {
    "support": BranchTemplate(
        name="support",
        node_type="evidence",
        relation="supports",
        default_status="active",
        description="Gather evidence or observations that strengthen an existing claim.",
        prompt_prefix="What evidence, source, or observation strengthens this claim?",
        edge_note="support branch",
    ),
    "objection": BranchTemplate(
        name="objection",
        node_type="objection",
        relation="contradicts",
        default_status="active",
        description="Pressure-test a claim by recording what could make it false or weak.",
        prompt_prefix="What weakens this claim or would change your mind about it?",
        edge_note="objection branch",
    ),
    "reframing": BranchTemplate(
        name="reframing",
        node_type="question",
        relation="refines",
        default_status="active",
        description="Reframe the inquiry when the current question may be too narrow or misplaced.",
        prompt_prefix="Is there a better question, frame, or interpretation to pursue from here?",
        edge_note="reframing branch",
    ),
    "application": BranchTemplate(
        name="application",
        node_type="claim",
        relation="derived_from",
        default_status="promising",
        description="Spin out a practical implication, downstream use, or design direction.",
        prompt_prefix="If this claim holds, what practical implication or next move follows?",
        edge_note="application branch",
    ),
}


def render_branch_content(parent_title: str, template: BranchTemplate, content: str | None) -> str:
    if content:
        return content
    return (
        f"{template.prompt_prefix}\n\n"
        f"Origin node: {parent_title}\n"
        "Why this branch exists:\n"
        "- \n"
        "What would make this branch stronger:\n"
        "- \n"
        "What would make this branch weaker:\n"
        "- "
    )


def build_branch_node(
    *,
    parent_title: str,
    template_name: str,
    title: str,
    content: str | None,
    citations: list[str],
    author: str,
    confidence: float,
    extra_tags: list[str],
) -> tuple[Node, BranchTemplate]:
    try:
        template = BRANCH_TEMPLATES[template_name]
    except KeyError as exc:
        valid = ", ".join(sorted(BRANCH_TEMPLATES))
        raise ValueError(f"Unknown template: {template_name}. Valid templates: {valid}") from exc

    tags = [f"branch:{template.name}", "template"] + extra_tags
    node = Node(
        node_type=template.node_type,  # type: ignore[arg-type]
        title=title,
        content=render_branch_content(parent_title, template, content),
        citations=citations,
        author=author,
        confidence=confidence,
        status=template.default_status,  # type: ignore[arg-type]
        tags=tags,
    )
    return node, template
