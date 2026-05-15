from __future__ import annotations

import importlib.util
import tempfile
import unittest
import sys
import types
from pathlib import Path
import xml.etree.ElementTree as ET


MODULE_PATH = Path(__file__).with_name("asce_parser.py")


def load_module():
    if "mcp.server.fastmcp" not in sys.modules:
        mcp_module = types.ModuleType("mcp")
        server_module = types.ModuleType("mcp.server")
        fastmcp_module = types.ModuleType("mcp.server.fastmcp")

        class FastMCP:
            def __init__(self, *_args, **_kwargs):
                pass

            def tool(self, *_args, **_kwargs):
                def decorator(func):
                    return func

                return decorator

        fastmcp_module.FastMCP = FastMCP
        server_module.fastmcp = fastmcp_module
        mcp_module.server = server_module
        sys.modules["mcp"] = mcp_module
        sys.modules["mcp.server"] = server_module
        sys.modules["mcp.server.fastmcp"] = fastmcp_module

    spec = importlib.util.spec_from_file_location("asce_parser_test_module", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load asce_parser module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_case(path: Path) -> None:
    path.write_text(
        """<?xml version="1.0" encoding="utf-8"?>
<asce>
  <nodes>
    <node reference="N1">
      <type>1</type>
      <user-title>Claim A</user-title>
      <status-fields>
        <status-field name="annotation" type="string">seed note</status-field>
      </status-fields>
    </node>
    <node reference="N2">
      <type>3</type>
      <user-title>Evidence B</user-title>
    </node>
  </nodes>
  <links>
    <link reference="L1">
      <type>1</type>
      <source-reference>N2</source-reference>
      <destination-reference>N1</destination-reference>
    </link>
    <link reference="L1-dup">
      <type>1</type>
      <source-reference>N2</source-reference>
      <destination-reference>N1</destination-reference>
    </link>
  </links>
</asce>
""",
        encoding="utf-8",
    )


def write_schema_case(path: Path, confidence: str) -> None:
    path.write_text(
        f"""<?xml version="1.0" encoding="utf-8"?>
<asce>
  <nodes>
    <node reference="N1">
      <type>1</type>
      <user-title>Claim A</user-title>
      <status-fields>
        <status-field name="confidence" type="string">{confidence}</status-field>
        <status-field name="annotation" type="string">seed note</status-field>
      </status-fields>
    </node>
  </nodes>
</asce>
""",
        encoding="utf-8",
    )


class AsceParserReconstructionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_module()
        self.module.ACTIVE_AXML_PATH = None

    def test_reconstruction_promotes_new_path_and_keeps_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            source_path = Path(tmpdir) / "case.axml"
            write_case(source_path)

            result = self.module.reconstruct_assurance_case(file_path=str(source_path))

            self.assertEqual(result["status"], "written")
            self.assertNotEqual(result["file_path"], str(source_path))
            self.assertTrue(Path(result["file_path"]).exists())
            self.assertEqual(self.module.ACTIVE_AXML_PATH, result["file_path"])

            parsed = self.module.parse_assurance_case()
            self.assertEqual(parsed["file_path"], result["file_path"])

            root_claims = self.module.get_root_claims()
            self.assertEqual(root_claims["file_path"], result["file_path"])
            self.assertEqual(root_claims["count"], 1)
            self.assertEqual(root_claims["root_claims"][0]["title"], "Claim A")

            graph = parsed["graph"]
            titles = {node["id"]: node["title"] for node in graph["nodes"]}
            self.assertEqual(titles["N1"], "Claim A")
            self.assertEqual(titles["N2"], "Evidence B")

    def test_reconstruction_dedupes_duplicate_links_and_uses_active_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            source_path = Path(tmpdir) / "case.axml"
            write_case(source_path)

            source_tree = ET.parse(source_path)
            self.assertEqual(len(source_tree.findall(".//link")), 2)

            result = self.module.reconstruct_assurance_case(file_path=str(source_path))
            reconstructed_tree = ET.parse(result["file_path"])

            self.assertEqual(len(reconstructed_tree.findall(".//link")), 1)
            children = self.module.get_node_children("N1")
            self.assertEqual(len(children["children"]), 1)
            self.assertEqual(children["children"][0]["id"], "N2")

    def test_bootstrap_case_creation_and_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            case_path = Path(tmpdir) / "bootstrap.axml"

            result = self.module.create_assurance_case(
                output_path=str(case_path),
                title="Demo bootstrap case",
                template_name="generic",
                system_name="Demo System",
                system_context="Demo operating context",
                strategy="hybrid",
            )

            self.assertEqual(result["status"], "written")
            self.assertTrue(Path(result["file_path"]).exists())

            validation = self.module.validate_case_structure(str(case_path))
            self.assertTrue(validation["valid"])
            self.assertGreaterEqual(validation["node_count"], 5)

            roots = self.module.get_root_claims(str(case_path))
            self.assertEqual(roots["count"], 1)
            self.assertIn("Demo System", roots["root_claims"][0]["title"])

            gaps = self.module.find_unresolved_gaps(str(case_path))
            self.assertGreaterEqual(gaps["count"], 1)

            summary = self.module.generate_case_summary(str(case_path))
            self.assertIn("Bootstrap summary", summary["summary"])

    def test_load_rejects_invalid_confidence_enum_value(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            source_path = Path(tmpdir) / "invalid.axml"
            write_schema_case(source_path, "medium")

            with self.assertRaisesRegex(
                ValueError,
                r"Invalid value 'medium' for status field 'confidence'",
            ):
                self.module.parse_assurance_case(str(source_path))

    def test_load_accepts_schema_valid_confidence_value(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            source_path = Path(tmpdir) / "valid.axml"
            write_schema_case(source_path, "Medium")

            parsed = self.module.parse_assurance_case(str(source_path))
            self.assertEqual(parsed["file_path"], str(source_path))
            graph_nodes = {node["id"]: node for node in parsed["graph"]["nodes"]}
            self.assertIn("N1", graph_nodes)
            self.assertEqual(graph_nodes["N1"]["title"], "Claim A")

    def test_bootstrap_links_flow_from_child_to_parent(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            case_path = Path(tmpdir) / "bootstrap.axml"

            self.module.create_assurance_case(output_path=str(case_path), title="Bootstrap case")
            root_claim = self.module.create_claim(title="Root claim", file_path=str(case_path))
            child_evidence = self.module.create_evidence_placeholder(
                title="Evidence A",
                file_path=str(case_path),
                parent_node_id=root_claim["node_id"],
            )

            tree = ET.parse(case_path)
            links = tree.findall(".//link")
            self.assertEqual(len(links), 1)
            self.assertEqual(links[0].findtext("source-reference"), child_evidence["node_id"])
            self.assertEqual(links[0].findtext("destination-reference"), root_claim["node_id"])

    def test_abstraction_layer_classification_covers_all_layers(self) -> None:
        module = self.module

        self.assertEqual(module._classify_abstraction_layer({"title": "Component interface"}), "Component")
        self.assertEqual(
            module._classify_abstraction_layer({"title": "Functional cluster boundary"}),
            "Functional Cluster",
        )
        self.assertEqual(module._classify_abstraction_layer({"title": "Runtime orchestration"}), "System")
        self.assertEqual(module._classify_abstraction_layer({"title": "Deployment scenario"}), "Scenario")

    def test_socratic_scoping_agent_contracts_are_present(self) -> None:
        agents_dir = Path(__file__).resolve().parents[1] / ".opencode" / "agents"
        orchestrator = (agents_dir / "pba-orchestrator.md").read_text(encoding="utf-8")
        provenance = (agents_dir / "provenance-inquisitor.md").read_text(encoding="utf-8")
        architecture = (agents_dir / "architecture-inquisitor.md").read_text(encoding="utf-8")
        resilience = (agents_dir / "resilience-inquisitor.md").read_text(encoding="utf-8")
        opencode_apply = (Path(__file__).resolve().parents[1] / ".opencode" / "commands" / "opsx-apply.md").read_text(encoding="utf-8")
        opencode_archive = (Path(__file__).resolve().parents[1] / ".opencode" / "commands" / "opsx-archive.md").read_text(encoding="utf-8")
        pi_apply = (Path(__file__).resolve().parents[1] / "extern" / "MITREThreatGraph" / ".pi" / "prompts" / "opsx-apply.md").read_text(encoding="utf-8")
        pi_archive = (Path(__file__).resolve().parents[1] / "extern" / "MITREThreatGraph" / ".pi" / "prompts" / "opsx-archive.md").read_text(encoding="utf-8")

        self.assertIn("document-driven route", orchestrator)
        self.assertIn("greenfield interview route", orchestrator)
        self.assertIn("Claim Extraction", orchestrator)
        self.assertIn("Strategy Decomposition", orchestrator)
        self.assertIn("Activity Mapping", orchestrator)
        self.assertIn("commercial_gap_type", orchestrator)
        self.assertIn("abstraction_layer", orchestrator)
        self.assertIn("Ask no more than two questions", orchestrator)

        self.assertIn("Class 1", provenance)
        self.assertIn("Class 2", architecture)
        self.assertIn("Class 3", resilience)
        self.assertIn("Ask at most two questions", provenance)
        self.assertIn("Ask at most two questions", architecture)
        self.assertIn("Ask at most two questions", resilience)
        self.assertIn("Do not suggest or propose", provenance)
        self.assertIn("Do not suggest or propose", architecture)
        self.assertIn("Do not recommend", resilience)

        for text in (opencode_apply, pi_apply):
            self.assertIn("Create and switch to a feature branch", text)
            self.assertIn("same branch", text)
            self.assertIn("Active branch or branch transition state", text)
            self.assertIn("dirty or branch creation fails", text)

        for text in (opencode_archive, pi_archive):
            self.assertIn("Finalize the branch transition", text)
            self.assertIn("change branch", text)
            self.assertIn("retained locally for manual cleanup", text)
            self.assertIn("Switch back to the base branch", text)


if __name__ == "__main__":
    unittest.main()
