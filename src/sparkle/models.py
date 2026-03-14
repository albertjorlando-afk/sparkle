from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
import hashlib
import json
from typing import Literal

NodeType = Literal[
    "claim",
    "evidence",
    "question",
    "objection",
    "inference",
    "decision",
    "synthesis",
]

NodeStatus = Literal[
    "active",
    "stalled",
    "weakly_supported",
    "promising",
    "abandoned",
    "harvested",
]


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


@dataclass(frozen=True)
class Node:
    node_type: NodeType
    title: str
    content: str
    citations: list[str] = field(default_factory=list)
    author: str = "local"
    created_at: str = field(default_factory=utc_now_iso)
    confidence: float = 0.5
    status: NodeStatus = "active"
    tags: list[str] = field(default_factory=list)

    def to_payload(self) -> dict:
        return asdict(self)

    def compute_id(self) -> str:
        canonical = json.dumps(self.to_payload(), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Edge:
    from_id: str
    to_id: str
    relation: str
    note: str = ""
    created_at: str = field(default_factory=utc_now_iso)

    def to_payload(self) -> dict:
        return asdict(self)

    def compute_id(self) -> str:
        canonical = json.dumps(self.to_payload(), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
