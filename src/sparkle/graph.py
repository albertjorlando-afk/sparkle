from __future__ import annotations

from collections import deque
import json
from pathlib import Path

from .models import Edge, Node


class GraphStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write({"nodes": {}, "edges": {}})

    def _read(self) -> dict:
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _write(self, payload: dict) -> None:
        self.path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    def init(self) -> None:
        if not self.path.exists():
            self._write({"nodes": {}, "edges": {}})

    def add_node(self, node: Node) -> str:
        data = self._read()
        node_id = node.compute_id()
        data["nodes"][node_id] = node.to_payload()
        self._write(data)
        return node_id

    def add_edge(self, edge: Edge) -> str:
        data = self._read()
        if edge.from_id not in data["nodes"]:
            raise ValueError(f"Unknown from_id: {edge.from_id}")
        if edge.to_id not in data["nodes"]:
            raise ValueError(f"Unknown to_id: {edge.to_id}")
        edge_id = edge.compute_id()
        data["edges"][edge_id] = edge.to_payload()
        self._write(data)
        return edge_id

    def list_nodes(self) -> list[tuple[str, dict]]:
        data = self._read()
        return sorted(data["nodes"].items(), key=lambda item: item[1]["created_at"])

    def list_edges(self) -> list[tuple[str, dict]]:
        data = self._read()
        return sorted(data["edges"].items(), key=lambda item: item[1]["created_at"])

    def resolve_id(self, prefix: str) -> str:
        data = self._read()
        matches = [node_id for node_id in data["nodes"] if node_id.startswith(prefix)]
        if not matches:
            raise ValueError(f"No node found for prefix: {prefix}")
        if len(matches) > 1:
            raise ValueError(f"Ambiguous prefix {prefix}: {', '.join(matches[:5])}")
        return matches[0]

    def get_node(self, node_id: str) -> dict:
        data = self._read()
        try:
            return data["nodes"][node_id]
        except KeyError as exc:
            raise ValueError(f"Unknown node: {node_id}") from exc

    def get_neighbors(self, node_id: str) -> dict[str, list[dict]]:
        data = self._read()
        inbound = []
        outbound = []
        for edge_id, edge in data["edges"].items():
            if edge["to_id"] == node_id:
                inbound.append({"edge_id": edge_id, **edge})
            if edge["from_id"] == node_id:
                outbound.append({"edge_id": edge_id, **edge})
        return {"inbound": inbound, "outbound": outbound}

    def lineage(self, root_id: str) -> list[tuple[str, dict]]:
        data = self._read()
        visited: set[str] = set()
        order: list[tuple[str, dict]] = []
        queue = deque([root_id])

        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            order.append((current, data["nodes"][current]))
            for edge in data["edges"].values():
                if edge["to_id"] == current:
                    queue.append(edge["from_id"])
        return order

    def subgraph(self, root_id: str) -> tuple[list[tuple[str, dict]], list[dict]]:
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

    def export_markdown(self, root_id: str, output: Path | None = None) -> str:
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
