from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
import xml.etree.ElementTree as ET


MODULE_PATH = Path(__file__).with_name("asce_parser.py")


def load_module():
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
      <source-reference>N1</source-reference>
      <destination-reference>N2</destination-reference>
    </link>
    <link reference="L1-dup">
      <type>1</type>
      <source-reference>N1</source-reference>
      <destination-reference>N2</destination-reference>
    </link>
  </links>
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


if __name__ == "__main__":
    unittest.main()
