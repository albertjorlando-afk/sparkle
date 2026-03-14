from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
import io
from pathlib import Path
import tempfile
import unittest

from src.sparkle.cli import main


class SparkleCliTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.store = Path(self.temp_dir.name) / "graph.json"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = main(["--store", str(self.store), *args])
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_init_and_bootstrap_seed_example_graph(self) -> None:
        exit_code, output, err = self.run_cli("init")
        self.assertEqual(exit_code, 0)
        self.assertIn("Initialized graph store", output)
        self.assertEqual(err, "")

        exit_code, output, err = self.run_cli("bootstrap")
        self.assertEqual(exit_code, 0)
        self.assertIn("Seeded concept graph", output)
        self.assertIn("root_claim_id:", output)
        self.assertEqual(err, "")

        exit_code, output, err = self.run_cli("list-nodes")
        self.assertEqual(exit_code, 0)
        self.assertIn("claim", output)
        self.assertIn("evidence", output)
        self.assertIn("synthesis", output)
        self.assertEqual(err, "")

    def test_add_node_add_edge_show_and_export(self) -> None:
        self.run_cli("init")

        exit_code, claim_out, _ = self.run_cli(
            "add-node",
            "--type",
            "claim",
            "--title",
            "Test claim",
            "--content",
            "A deterministic graph should preserve provenance.",
            "--status",
            "promising",
            "--confidence",
            "0.8",
        )
        self.assertEqual(exit_code, 0)
        claim_id = claim_out.strip().split()[-1]

        exit_code, evidence_out, _ = self.run_cli(
            "add-node",
            "--type",
            "evidence",
            "--title",
            "Test evidence",
            "--content",
            "The archived discussion explicitly argues for provenance and branching.",
            "--citations",
            "archive/chatgpt-merkle-dag-research.md",
        )
        self.assertEqual(exit_code, 0)
        evidence_id = evidence_out.strip().split()[-1]

        exit_code, output, err = self.run_cli(
            "add-edge",
            "--from",
            evidence_id[:12],
            "--to",
            claim_id[:12],
            "--relation",
            "supports",
        )
        self.assertEqual(exit_code, 0)
        self.assertIn("Added edge", output)
        self.assertEqual(err, "")

        exit_code, output, err = self.run_cli("show", claim_id[:12])
        self.assertEqual(exit_code, 0)
        self.assertIn("Title: Test claim", output)
        self.assertIn("Inbound:", output)
        self.assertIn("-[supports]->", output)
        self.assertEqual(err, "")

        export_path = Path(self.temp_dir.name) / "exports" / "claim.md"
        exit_code, output, err = self.run_cli(
            "export",
            "--root",
            claim_id[:12],
            "--output",
            str(export_path),
        )
        self.assertEqual(exit_code, 0)
        self.assertIn("Exported markdown", output)
        self.assertEqual(err, "")
        rendered = export_path.read_text(encoding="utf-8")
        self.assertIn("# Test claim", rendered)
        self.assertIn("## Edges", rendered)

    def test_lineage_walks_inbound_graph(self) -> None:
        self.run_cli("init")

        _, claim_out, _ = self.run_cli(
            "add-node",
            "--type",
            "claim",
            "--title",
            "Root claim",
            "--content",
            "Root content",
        )
        claim_id = claim_out.strip().split()[-1]

        _, question_out, _ = self.run_cli(
            "add-node",
            "--type",
            "question",
            "--title",
            "Open question",
            "--content",
            "What would strengthen the claim?",
        )
        question_id = question_out.strip().split()[-1]

        _, synthesis_out, _ = self.run_cli(
            "add-node",
            "--type",
            "synthesis",
            "--title",
            "Working synthesis",
            "--content",
            "A tested graph is easier to trust.",
        )
        synthesis_id = synthesis_out.strip().split()[-1]

        self.run_cli(
            "add-edge",
            "--from",
            question_id[:12],
            "--to",
            claim_id[:12],
            "--relation",
            "refines",
        )
        self.run_cli(
            "add-edge",
            "--from",
            claim_id[:12],
            "--to",
            synthesis_id[:12],
            "--relation",
            "derived_from",
        )

        exit_code, output, err = self.run_cli("lineage", synthesis_id[:12])
        self.assertEqual(exit_code, 0)
        self.assertIn("Working synthesis", output)
        self.assertIn("Root claim", output)
        self.assertIn("Open question", output)
        self.assertEqual(err, "")

    def test_unknown_prefix_returns_nonzero_and_stderr(self) -> None:
        self.run_cli("init")
        exit_code, output, err = self.run_cli("show", "missing")
        self.assertEqual(exit_code, 2)
        self.assertEqual(output, "")
        self.assertIn("No node found for prefix", err)


if __name__ == "__main__":
    unittest.main()
