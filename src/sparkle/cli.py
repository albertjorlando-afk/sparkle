from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .bootstrap import seed_concept_graph
from .graph import GraphStore
from .models import Edge, Node
from .templates import BRANCH_TEMPLATES, build_branch_node

DEFAULT_STORE = Path(".sparkle/graph.json")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sparkle claim-graph MVP")
    parser.add_argument("--store", type=Path, default=DEFAULT_STORE, help="Path to graph store JSON file")

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init", help="Initialize the local graph store")
    subparsers.add_parser("list-nodes", help="List nodes in the graph")
    subparsers.add_parser("list-edges", help="List edges in the graph")
    subparsers.add_parser("bootstrap", help="Seed the store from the archived concept conversation")
    subparsers.add_parser("list-templates", help="List structured branch templates")

    add_node = subparsers.add_parser("add-node", help="Add a typed node")
    add_node.add_argument("--type", required=True, dest="node_type")
    add_node.add_argument("--title", required=True)
    add_node.add_argument("--content", required=True)
    add_node.add_argument("--citations", nargs="*", default=[])
    add_node.add_argument("--author", default="local")
    add_node.add_argument("--confidence", type=float, default=0.5)
    add_node.add_argument("--status", default="active")
    add_node.add_argument("--tags", nargs="*", default=[])

    add_edge = subparsers.add_parser("add-edge", help="Link two nodes")
    add_edge.add_argument("--from", required=True, dest="from_id")
    add_edge.add_argument("--to", required=True, dest="to_id")
    add_edge.add_argument("--relation", required=True)
    add_edge.add_argument("--note", default="")

    add_branch = subparsers.add_parser("add-branch", help="Create a structured inquiry branch from an existing node")
    add_branch.add_argument("--from", required=True, dest="from_id")
    add_branch.add_argument("--template", required=True)
    add_branch.add_argument("--title", required=True)
    add_branch.add_argument("--content")
    add_branch.add_argument("--citations", nargs="*", default=[])
    add_branch.add_argument("--author", default="local")
    add_branch.add_argument("--confidence", type=float, default=0.5)
    add_branch.add_argument("--tags", nargs="*", default=[])

    show = subparsers.add_parser("show", help="Show a node with inbound and outbound edges")
    show.add_argument("node_id")

    lineage = subparsers.add_parser("lineage", help="Trace inbound lineage for a node")
    lineage.add_argument("node_id")

    export = subparsers.add_parser("export", help="Export a subgraph to markdown")
    export.add_argument("--root", required=True, dest="root_id")
    export.add_argument("--output", type=Path)

    return parser


def print_node_summary(node_id: str, node: dict) -> None:
    print(
        f"{node_id[:12]}  {node['node_type']:<10}  {node['status']:<16}  "
        f"{node['confidence']:.2f}  {node['title']}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    store = GraphStore(args.store)

    try:
        if args.command == "init":
            store.init()
            print(f"Initialized graph store at {args.store}")
            return 0

        if args.command == "bootstrap":
            ids = seed_concept_graph(store)
            print("Seeded concept graph from archived conversation")
            for label, node_id in ids.items():
                print(f"{label}: {node_id}")
            return 0

        if args.command == "list-templates":
            for name in sorted(BRANCH_TEMPLATES):
                template = BRANCH_TEMPLATES[name]
                print(
                    f"{template.name:<12} {template.node_type:<10} "
                    f"{template.relation:<12} {template.description}"
                )
            return 0

        if args.command == "add-node":
            node = Node(
                node_type=args.node_type,
                title=args.title,
                content=args.content,
                citations=args.citations,
                author=args.author,
                confidence=args.confidence,
                status=args.status,
                tags=args.tags,
            )
            node_id = store.add_node(node)
            print(f"Added node {node_id}")
            return 0

        if args.command == "add-edge":
            from_id = store.resolve_id(args.from_id)
            to_id = store.resolve_id(args.to_id)
            edge = Edge(from_id=from_id, to_id=to_id, relation=args.relation, note=args.note)
            edge_id = store.add_edge(edge)
            print(f"Added edge {edge_id}")
            return 0

        if args.command == "add-branch":
            from_id = store.resolve_id(args.from_id)
            parent_node = store.get_node(from_id)
            branch_node, template = build_branch_node(
                parent_title=parent_node["title"],
                template_name=args.template,
                title=args.title,
                content=args.content,
                citations=args.citations,
                author=args.author,
                confidence=args.confidence,
                extra_tags=args.tags,
            )
            branch_id = store.add_node(branch_node)
            edge_id = store.add_edge(
                Edge(
                    from_id=branch_id,
                    to_id=from_id,
                    relation=template.relation,
                    note=template.edge_note,
                )
            )
            print(f"Added branch node {branch_id}")
            print(f"Added branch edge {edge_id}")
            return 0

        if args.command == "list-nodes":
            nodes = store.list_nodes()
            if not nodes:
                print("No nodes found")
                return 0
            for node_id, node in nodes:
                print_node_summary(node_id, node)
            return 0

        if args.command == "list-edges":
            edges = store.list_edges()
            if not edges:
                print("No edges found")
                return 0
            for edge_id, edge in edges:
                print(
                    f"{edge_id[:12]}  {edge['from_id'][:10]} -[{edge['relation']}]-> "
                    f"{edge['to_id'][:10]}"
                )
            return 0

        if args.command == "show":
            node_id = store.resolve_id(args.node_id)
            node = store.get_node(node_id)
            neighbors = store.get_neighbors(node_id)

            print(f"ID: {node_id}")
            print(f"Type: {node['node_type']}")
            print(f"Title: {node['title']}")
            print(f"Status: {node['status']}")
            print(f"Confidence: {node['confidence']}")
            if node["tags"]:
                print(f"Tags: {', '.join(node['tags'])}")
            if node["citations"]:
                print(f"Citations: {', '.join(node['citations'])}")
            print("")
            print(node["content"])
            print("")
            print("Inbound:")
            for edge in neighbors["inbound"]:
                print(f"- {edge['from_id'][:10]} -[{edge['relation']}]-> {node_id[:10]}")
            print("Outbound:")
            for edge in neighbors["outbound"]:
                print(f"- {node_id[:10]} -[{edge['relation']}]-> {edge['to_id'][:10]}")
            return 0

        if args.command == "lineage":
            node_id = store.resolve_id(args.node_id)
            for ancestor_id, ancestor in store.lineage(node_id):
                print_node_summary(ancestor_id, ancestor)
            return 0

        if args.command == "export":
            root_id = store.resolve_id(args.root_id)
            rendered = store.export_markdown(root_id, args.output)
            if args.output:
                print(f"Exported markdown to {args.output}")
            else:
                print(rendered)
            return 0

        parser.print_help()
        return 1
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
