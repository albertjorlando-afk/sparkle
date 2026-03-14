from __future__ import annotations

from .graph import GraphStore
from .models import Edge, Node


def seed_concept_graph(store: GraphStore) -> dict[str, str]:
    concept_reference = "https://chatgpt.com/c/69b579e3-3cf8-8331-8d8d-185381cbbb01"

    root_claim = Node(
        node_type="claim",
        title="A claim-graph research tool can use Merkle-style provenance",
        content=(
            "A solo research tool can model inquiry as a claim graph while using content-addressed "
            "storage underneath to preserve provenance, branch paths, and selective extraction."
        ),
        citations=[concept_reference],
        confidence=0.82,
        status="promising",
        tags=["origin", "product-idea"],
    )
    root_claim_id = store.add_node(root_claim)

    evidence = Node(
        node_type="evidence",
        title="Original conversation identifies provenance and branching benefits",
        content=(
            "The original concept conversation explicitly highlights provenance, branching without loss, "
            "reproducibility, and selective extraction as core advantages."
        ),
        citations=[concept_reference],
        confidence=0.9,
        status="active",
        tags=["origin"],
    )
    evidence_id = store.add_node(evidence)

    question = Node(
        node_type="question",
        title="What is the smallest usable solo workflow?",
        content=(
            "The product should prove that a solo researcher can create a claim, attach evidence and objections, "
            "trace lineage, and export a selected path into a usable document."
        ),
        citations=[concept_reference],
        confidence=0.74,
        status="active",
        tags=["mvp"],
    )
    question_id = store.add_node(question)

    objection = Node(
        node_type="objection",
        title="Capturing every thought could create unusable noise",
        content=(
            "If the tool models every micro-thought as immutable history, the graph can become noisy and stop "
            "feeling like a research environment."
        ),
        citations=[concept_reference],
        confidence=0.88,
        status="active",
        tags=["risk"],
    )
    objection_id = store.add_node(objection)

    synthesis = Node(
        node_type="synthesis",
        title="The product should expose a claim graph over immutable provenance objects",
        content=(
            "The conversation's strongest framing is to keep the user-facing model as a claim graph while the "
            "storage model remains a Merkle-style DAG. That preserves rigor without forcing Git-like mental models."
        ),
        citations=[concept_reference],
        confidence=0.86,
        status="harvested",
        tags=["direction"],
    )
    synthesis_id = store.add_node(synthesis)

    store.add_edge(Edge(from_id=evidence_id, to_id=root_claim_id, relation="supports"))
    store.add_edge(Edge(from_id=question_id, to_id=root_claim_id, relation="refines"))
    store.add_edge(Edge(from_id=objection_id, to_id=root_claim_id, relation="contradicts"))
    store.add_edge(Edge(from_id=root_claim_id, to_id=synthesis_id, relation="derived_from"))
    store.add_edge(Edge(from_id=objection_id, to_id=synthesis_id, relation="refines", note="motivates layered working views"))

    return {
        "root_claim_id": root_claim_id,
        "evidence_id": evidence_id,
        "question_id": question_id,
        "objection_id": objection_id,
        "synthesis_id": synthesis_id,
    }
