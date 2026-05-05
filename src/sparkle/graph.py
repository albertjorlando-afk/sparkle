from __future__ import annotations

from collections import deque
import json
from pathlib import Path
from typing import Any

from .models import DEFAULT_EDGE_RELATIONS, DEFAULT_NODE_TYPES, Edge, Node


class GraphStore:
    def __init__(
        self,
        path: str | Path,
        *,
        node_types: set[str] | None = None,
        edge_relations: set[str] | None = None,
    ) -> None:
        self.node_types = node_types or DEFAULT_NODE_TYPES
        self.edge_relations = edge_relations or DEFAULT_EDGE_RELATIONS
        self.path = path
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write({"nodes": {}, "edges": {}})

    def _read(self) -> dict[str, Any]:
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            raise ValueError(f"Corrupt graph store at {self.path}: {e}") from e
        if not isinstance(data, dict) or not isinstance(data.get("nodes"), dict) or not isinstance(data.get("edges"), dict):
            raise ValueError(f"Invalid graph store at {self.path}")
        return data

    def _write(self, payload: dict[str, Any]) -> None:
        self.path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    def init(self) -> None:
        if not self.path.exists():
            self._write({"nodes": {}, "edges": {}})

    def add_node(self, node: Node) -> str:
        self._validate_node(node)
        data = self._read()
        node_id = node.compute_id()
        data["nodes"][node_id] = node.to_payload()
        self._write(data)
        return node_id

    def add_node_payload(self, payload: dict[str, Any]) -> str:
        return self.add_node(Node(**payload))

    def add_edge(self, edge: Edge) -> str:
        self._validate_edge(edge)
        data = self._read()
        if edge.from_id not in data["nodes"]:
            raise ValueError(f"Unknown from_id: {edge.from_id}")
        if edge.to_id not in data["nodes"]:
            raise ValueError(f"Unknown to_id: {edge.to_id}")
        edge_id = edge.compute_id()
        data["edges"][edge_id] = edge.to_payload()
        self._write(data)
        return edge_id

    def add_edge_payload(self, payload: dict[str, Any]) -> str:
        return self.add_edge(Edge(**payload))

    def read(self) -> dict[str, Any]:
        return self._read()

    def list_nodes(
        self,
        *,
        node_type: str | None = None,
        status: str | None = None,
        tag: str | None = None,
        query: str | None = None,
    ) -> list[tuple[str, dict[str, Any]]]:
        data = self._read()
        nodes = sorted(data["nodes"].items(), key=lambda item: item[1].get("created_at", ""))
        output = []
        for node_id, node in nodes:
            if node_type and node.get("node_type") != node_type:
                continue
            if status and node.get("status") != status:
                continue
            if tag and tag not in node.get("tags", []):
                continue
            if query:
                haystack = " ".join(
                    [
                        str(node.get("title", "")),
                        str(node.get("content", "")),
                        " ".join(node.get("tags", [])),
                        " ".join(node.get("citations", [])),
                    ]
                ).lower()
                if query.lower() not in haystack:
                    continue
            output.append((node_id, node))
        return output

    def list_edges(self) -> list[tuple[str, dict[str, Any]]]:
        data = self._read()
        return sorted(data["edges"].items(), key=lambda item: item[1].get("created_at", ""))

    def resolve_id(self, prefix: str) -> str:
        data = self._read()
        if prefix in data["nodes"]:
            return prefix
        matches = [node_id for node_id in data["nodes"] if node_id.startswith(prefix)]
        if not matches:
            raise ValueError(f"No node found for prefix: {prefix}")
        if len(matches) > 1:
            raise ValueError(f"Ambiguous prefix {prefix}: {', '.join(matches[:5])}")
        return matches[0]

    def get_node(self, node_id_or_prefix: str) -> dict[str, Any]:
        node_id = self.resolve_id(node_id_or_prefix)
        data = self._read()
        try:
            return data["nodes"][node_id]
        except KeyError as exc:
            raise ValueError(f"Unknown node: {node_id}") from exc

    def get_neighbors(self, node_id_or_prefix: str) -> dict[str, list[dict[str, Any]]]:
        node_id = self.resolve_id(node_id_or_prefix)
        data = self._read()
        inbound = []
        outbound = []
        for edge_id, edge in data["edges"].items():
            if edge["to_id"] == node_id:
                inbound.append({"edge_id": edge_id, **edge})
            if edge["from_id"] == node_id:
                outbound.append({"edge_id": edge_id, **edge})
        return {"inbound": inbound, "outbound": outbound}

    def get_neighbor_details(self, node_id_or_prefix: str) -> dict[str, list[dict[str, Any]]]:
        node_id = self.resolve_id(node_id_or_prefix)
        data = self._read()
        inbound = []
        outbound = []
        for edge_id, edge in data["edges"].items():
            if edge["to_id"] == node_id:
                if edge["from_id"] not in data["nodes"]:
                    continue
                related_node = data["nodes"][edge["from_id"]]
                inbound.append({"edge_id": edge_id, "node_id": edge["from_id"], "node": related_node, **edge})
            if edge["from_id"] == node_id:
                if edge["to_id"] not in data["nodes"]:
                    continue
                related_node = data["nodes"][edge["to_id"]]
                outbound.append({"edge_id": edge_id, "node_id": edge["to_id"], "node": related_node, **edge})
        inbound.sort(key=lambda item: (item["relation"], item["node"]["title"]))
        outbound.sort(key=lambda item: (item["relation"], item["node"]["title"]))
        return {"inbound": inbound, "outbound": outbound}

    def lineage(self, root_id_or_prefix: str) -> list[tuple[str, dict[str, Any]]]:
        root_id = self.resolve_id(root_id_or_prefix)
        data = self._read()
        visited: set[str] = set()
        order: list[tuple[str, dict]] = []
        queue = deque([root_id])

        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            if current not in data["nodes"]:
                continue
            order.append((current, data["nodes"][current]))
            for edge in data["edges"].values():
                if edge["to_id"] == current:
                    queue.append(edge["from_id"])
        return order

    def subgraph(self, root_id_or_prefix: str) -> tuple[list[tuple[str, dict[str, Any]]], list[dict[str, Any]]]:
        root_id = self.resolve_id(root_id_or_prefix)
        data = self._read()
        visited: set[str] = set()
        queue = deque([root_id])

        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            for edge in data["edges"].values():
                if edge["from_id"] == current or edge["to_id"] == current:
                    queue.append(edge["from_id"])
                    queue.append(edge["to_id"])

        nodes = [(node_id, data["nodes"][node_id]) for node_id in visited]
        nodes.sort(key=lambda item: item[1]["created_at"])
        edges = [
            {"edge_id": edge_id, **edge}
            for edge_id, edge in data["edges"].items()
            if edge["from_id"] in visited and edge["to_id"] in visited
        ]
        edges.sort(key=lambda item: item["created_at"])
        return nodes, edges

    def export_markdown(self, root_id_or_prefix: str, output: Path | None = None) -> str:
        root_id = self.resolve_id(root_id_or_prefix)
        nodes, edges = self.subgraph(root_id)
        root = self.get_node(root_id)

        lines = [
            f"# {root['title']}",
            "",
            f"- Root node: `{root_id}`",
            f"- Type: `{root['node_type']}`",
            f"- Status: `{root['status']}`",
            f"- Confidence: `{root['confidence']}`",
            "",
            "## Root claim",
            "",
            root["content"],
            "",
            "## Nodes",
            "",
        ]

        for node_id, node in nodes:
            lines.extend(
                [
                    f"### {node['title']}",
                    "",
                    f"- ID: `{node_id}`",
                    f"- Type: `{node['node_type']}`",
                    f"- Status: `{node['status']}`",
                    f"- Confidence: `{node['confidence']}`",
                ]
            )
            if node["citations"]:
                lines.append(f"- Citations: {', '.join(node['citations'])}")
            lines.extend(["", node["content"], ""])

        lines.extend(["## Edges", ""])
        for edge in edges:
            lines.append(
                f"- `{edge['from_id'][:10]}` -[{edge['relation']}]-> `{edge['to_id'][:10]}`"
                + (f" ({edge['note']})" if edge["note"] else "")
            )

        rendered = "\n".join(lines) + "\n"
        if output is not None:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(rendered, encoding="utf-8")
        return rendered

    def render_tree(self, root_id_or_prefix: str) -> str:
        root_id = self.resolve_id(root_id_or_prefix)
        data = self._read()
        root = data["nodes"][root_id]
        lines = [f"{root['node_type']} {root_id[:12]}  {root['title']}"]

        inbound = []
        outbound = []
        for edge_id, edge in data["edges"].items():
            if edge["to_id"] == root_id and edge["from_id"] in data["nodes"]:
                related_node = data["nodes"][edge["from_id"]]
                inbound.append({"edge_id": edge_id, "node_id": edge["from_id"], "node": related_node, **edge})
            if edge["from_id"] == root_id and edge["to_id"] in data["nodes"]:
                related_node = data["nodes"][edge["to_id"]]
                outbound.append({"edge_id": edge_id, "node_id": edge["to_id"], "node": related_node, **edge})
        inbound.sort(key=lambda item: (item["relation"], item["node"]["title"]))
        outbound.sort(key=lambda item: (item["relation"], item["node"]["title"]))

        def append_branch(title: str, items: list[dict]) -> None:
            if not items:
                return
            lines.append(f"{title}:")
            for index, item in enumerate(items):
                connector = "└─" if index == len(items) - 1 else "├─"
                lines.append(
                    f"{connector} {item['relation']:<12} {item['node']['node_type']:<10} "
                    f"{item['node_id'][:12]}  {item['node']['title']}"
                )

        append_branch("Incoming", inbound)
        append_branch("Outgoing", outbound)
        return "\n".join(lines) + "\n"

    def render_why(self, root_id_or_prefix: str) -> str:
        root_id = self.resolve_id(root_id_or_prefix)
        data = self._read()
        root = data["nodes"][root_id]
        lines = [f"{root['node_type']} {root_id[:12]}  {root['title']}"]
        visited: set[str] = set()

        def walk(node_id: str, prefix: str) -> None:
            if node_id in visited:
                return
            visited.add(node_id)
            inbound = []
            for edge_id, edge in data["edges"].items():
                if edge["to_id"] == node_id and edge["from_id"] in data["nodes"]:
                    related_node = data["nodes"][edge["from_id"]]
                    inbound.append({"edge_id": edge_id, "node_id": edge["from_id"], "node": related_node, **edge})
            inbound.sort(key=lambda item: (item["relation"], item["node"]["title"]))
            for item in inbound:
                lines.append(
                    f"{prefix}<- {item['relation']:<12} {item['node']['node_type']:<10} "
                    f"{item['node_id'][:12]}  {item['node']['title']}"
                )
                walk(item["node_id"], prefix + "   ")

        walk(root_id, "")
        return "\n".join(lines) + "\n"

    def export(self, node_id_or_prefix: str) -> dict[str, Any]:
        root_id = self.resolve_id(node_id_or_prefix)
        lineage_ids = {node_id for node_id, _ in self.lineage(root_id)}
        data = self._read()
        return {
            "root_id": root_id,
            "nodes": {node_id: data["nodes"][node_id] for node_id in sorted(lineage_ids)},
            "edges": {
                edge_id: edge
                for edge_id, edge in data["edges"].items()
                if edge["from_id"] in lineage_ids and edge["to_id"] in lineage_ids
            },
        }

    def _validate_node(self, node: Node) -> None:
        if node.node_type not in self.node_types:
            raise ValueError(f"unknown node_type: {node.node_type}")

    def _validate_edge(self, edge: Edge) -> None:
        if edge.relation not in self.edge_relations:
            raise ValueError(f"unknown edge relation: {edge.relation}")
