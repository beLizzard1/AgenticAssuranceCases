from __future__ import annotations

from functools import lru_cache
from datetime import datetime, timezone
import hashlib
import json
import sys
import shutil
from pathlib import Path
from typing import Any, Optional
import xml.etree.ElementTree as ET

import networkx as nx
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP

MCP_SERVER_DIR = Path(__file__).resolve().parent
if str(MCP_SERVER_DIR) not in sys.path:
    sys.path.insert(0, str(MCP_SERVER_DIR))

from bootstrap.templates import (
    get_bootstrap_pattern as _get_bootstrap_pattern,
    list_bootstrap_patterns as _list_bootstrap_patterns,
    render_bootstrap_pattern as _render_bootstrap_pattern,
)


REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schemas" / "ASCAD 2.0.xml"

MCP_SERVER_NAME = "asce_tools"
mcp = FastMCP(MCP_SERVER_NAME)
MCP_FINGERPRINT = "asce_parser_v1.0.3_abc123"
MODEL_USED = "gpt-5.4-mini"
SHARED_AGENT_CONTEXT = {"system_brief": "No context provided yet."}
ACTIVE_AXML_PATH: str | None = None
EVIDENCE_PROVIDER_REGISTRY: dict[str, dict[str, Any]] = {}

TITLE_TAGS = ("user-title", "title", "name", "label")
ANNOTATION_TAGS = ("annotation", "annotations", "comment", "description", "notes", "html")
ID_ATTRS = ("reference", "id", "xml:id", "guid", "uid", "nodeid", "node_id")
RELATION_ATTRS = ("source", "target", "from", "to", "ref", "refid", "parent", "child")

TYPE_CODE_MAP = {
    "1": "claim",
    "2": "argument",
    "3": "evidence",
    "4": "other",
    "5": "caption",
    "6": "side-claim",
    "7": "subcase",
    "8": "defeater",
    "9": "comment",
}

NODE_TYPE_CODE_MAP = {value: key for key, value in TYPE_CODE_MAP.items()}


def _local_name(tag: str) -> str:
    if tag.startswith("{"):
        return tag.rsplit("}", 1)[-1]
    if ":" in tag:
        return tag.split(":", 1)[1]
    return tag


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).split())


def _normalize_capabilities(capabilities: Any) -> list[str]:
    if capabilities is None:
        return []
    if isinstance(capabilities, str):
        items = [capabilities]
    else:
        items = list(capabilities)

    normalized = []
    for item in items:
        text = _normalize_text(item)
        if text:
            normalized.append(text)
    return sorted(set(normalized))


def _schema_node_type_code(node_type: str) -> str:
    normalized = _normalize_text(node_type).lower()
    if normalized in NODE_TYPE_CODE_MAP:
        return NODE_TYPE_CODE_MAP[normalized]
    if normalized.isdigit() and normalized in TYPE_CODE_MAP:
        return normalized
    return NODE_TYPE_CODE_MAP["other"]


def _schema_node_type_key(node_type: str) -> str:
    normalized = _normalize_text(node_type)
    if normalized in TYPE_CODE_MAP:
        return TYPE_CODE_MAP[normalized]
    lowered = normalized.lower()
    if lowered in NODE_TYPE_CODE_MAP:
        return lowered
    return "other"


def register_evidence_provider(
    name: str,
    description: str,
    capabilities: Any = None,
    tool_prefix: str | None = None,
    source_type: str = "mcp",
    status: str = "available",
) -> None:
    provider_name = _normalize_text(name)
    if not provider_name:
        raise ValueError("Provider name is required")

    EVIDENCE_PROVIDER_REGISTRY[provider_name] = {
        "name": provider_name,
        "description": _normalize_text(description),
        "capabilities": _normalize_capabilities(capabilities),
        "tool_prefix": _normalize_text(tool_prefix) or f"{provider_name}_*",
        "source_type": _normalize_text(source_type) or "mcp",
        "status": _normalize_text(status) or "available",
    }


def _provider_matches(provider: dict[str, Any], query: str | None = None, capability: str | None = None) -> bool:
    if capability:
        needle = _normalize_text(capability).lower()
        haystack = " ".join(provider.get("capabilities", [])).lower()
        if needle not in haystack:
            return False

    if query:
        needle = _normalize_text(query).lower()
        if needle:
            fields = [
                provider.get("name", ""),
                provider.get("description", ""),
                " ".join(provider.get("capabilities", [])),
                provider.get("tool_prefix", ""),
            ]
            haystack = " ".join(fields).lower()
            if needle not in haystack:
                return False

    return True


def _remember_active_axml_path(file_path: str | Path) -> str:
    global ACTIVE_AXML_PATH
    ACTIVE_AXML_PATH = str(Path(file_path))
    return ACTIVE_AXML_PATH


def _resolve_file_path(file_path: str | None) -> str:
    resolved = _normalize_text(file_path)
    if resolved:
        return _remember_active_axml_path(resolved)

    if ACTIVE_AXML_PATH:
        return ACTIVE_AXML_PATH

    raise ValueError("file_path is required until a reconstructed case has been selected")


register_evidence_provider(
    "asce_tools",
    "Schema-aware ASCE parser, neighborhood, registry, and write-back tools",
    capabilities=[
        "create_assurance_case",
        "list_bootstrap_patterns",
        "get_bootstrap_pattern",
        "instantiate_pattern",
        "create_claim",
        "create_context",
        "create_assumption",
        "create_evidence_placeholder",
        "create_defeater",
        "create_link",
        "find_unresolved_gaps",
        "generate_case_summary",
        "validate_case_structure",
        "parse_assurance_case",
        "get_assurance_neighborhood",
        "get_root_claims",
        "get_node_children",
        "reconstruct_assurance_case",
        "write_defeater",
        "modify_assurance_case",
        "set_system_context",
        "get_system_context",
        "discover_evidence_providers",
        "list_evidence_providers",
    ],
    tool_prefix="asce_tools_*",
)


def _strip_html(value: str) -> str:
    if not value:
        return ""
    return BeautifulSoup(value, "html.parser").get_text(" ", strip=True)


def _split_refs(value: str) -> list[str]:
    refs: list[str] = []
    for chunk in str(value).replace(",", " ").split():
        item = chunk.strip()
        if item:
            refs.append(item)
    return refs


def create_backup(file_path: str) -> str | None:
    """Create a timestamped backup before mutating an assurance-case file."""
    source = Path(file_path)
    if not source.exists():
        return None

    backup_dir = source.parent / ".backups"
    backup_dir.mkdir(exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%fZ")
    backup_path = backup_dir / f"{source.name}.{timestamp}.bak"
    shutil.copy2(source, backup_path)
    return str(backup_path)


@lru_cache(maxsize=1)
def load_schema_metadata() -> dict[str, Any]:
    metadata: dict[str, Any] = {
        "path": str(SCHEMA_PATH),
        "exists": SCHEMA_PATH.exists(),
        "name": None,
        "version": None,
        "requires_asce_version": None,
        "node_types": {},
        "link_types": {},
        "status_fields": {},
    }

    if not SCHEMA_PATH.exists():
        return metadata

    tree = ET.parse(str(SCHEMA_PATH))
    root = tree.getroot()
    metadata["name"] = _normalize_text(root.findtext("name"))
    metadata["version"] = _normalize_text(root.findtext("version"))
    metadata["requires_asce_version"] = _normalize_text(root.findtext("requiresasceversion"))

    for nodetype in root.findall("./nodetypes/nodetype"):
        key = _normalize_text(nodetype.findtext("key"))
        if not key:
            continue
        metadata["node_types"][key] = {
            "displaytext": _normalize_text(nodetype.findtext("displaytext")),
            "baseshape": _normalize_text(nodetype.findtext("baseshape")),
            "basecolour": _normalize_text(nodetype.findtext("basecolour")),
            "defaultlinktype": _normalize_text(nodetype.findtext("defaultlinktype")),
            "aspectratio": _normalize_text(nodetype.findtext("aspectratio")),
        }

    for linktype in root.findall("./linktypes/linktype"):
        key = _normalize_text(linktype.findtext("key"))
        if not key:
            continue
        metadata["link_types"][key] = {
            "displaytextforwards": _normalize_text(linktype.findtext("displaytextforwards")),
            "displaytextreversed": _normalize_text(linktype.findtext("displaytextreversed")),
            "reversed": _normalize_text(linktype.findtext("reversed")),
            "colour": _normalize_text(linktype.findtext("colour")),
        }

    for status_field in root.findall("./nodestatusfields/statusfield"):
        key = _normalize_text(status_field.findtext("key"))
        if not key:
            continue
        metadata["status_fields"][key] = {
            "displaytext": _normalize_text(status_field.findtext("displaytext")),
            "datatype": _normalize_text(status_field.findtext("datatype")),
            "default": _normalize_text(status_field.findtext("default")),
            "enumlist": _normalize_text(status_field.findtext("enumlist")),
        }

    return metadata


def _schema_type_name(node: ET.Element) -> str:
    type_code = _normalize_text(node.attrib.get("type") or node.findtext("type"))
    if type_code in TYPE_CODE_MAP:
        return TYPE_CODE_MAP[type_code]

    node_type = _normalize_text(node.attrib.get("nodetype") or node.findtext("nodetype"))
    if node_type:
        return node_type

    return _local_name(node.tag)


def _element_id(element: ET.Element, path: str) -> str:
    for attr in ID_ATTRS:
        value = _normalize_text(element.attrib.get(attr))
        if value:
            return value
    return path


def _extract_status_fields(element: ET.Element, schema: dict[str, Any]) -> dict[str, str]:
    status_fields: dict[str, str] = {}

    for child in list(element):
        child_tag = _local_name(child.tag).lower()
        if child_tag not in {"status-fields", "statusfield", "status-field"}:
            continue

        for status_child in list(child):
            key = _normalize_text(
                status_child.attrib.get("name")
                or status_child.attrib.get("key")
                or status_child.findtext("key")
            )
            value = _normalize_text(" ".join(status_child.itertext()))
            if key and value:
                status_fields[key] = value

    for key in schema.get("status_fields", {}):
        if key in element.attrib:
            status_fields[key] = _normalize_text(element.attrib.get(key))

    return status_fields


def _extract_title(element: ET.Element) -> str:
    for attr in ("title", "name", "label"):
        value = _normalize_text(element.attrib.get(attr))
        if value:
            return value

    for child in list(element):
        if _local_name(child.tag).lower() in TITLE_TAGS:
            value = _normalize_text(" ".join(child.itertext()))
            if value:
                return value

    return _normalize_text(element.attrib.get("text") or " ".join(element.itertext()))


def _extract_annotation(element: ET.Element) -> str:
    for child in list(element):
        if _local_name(child.tag).lower() in ANNOTATION_TAGS:
            value = _normalize_text(" ".join(child.itertext()))
            if value:
                return value

    return _strip_html(_normalize_text(" ".join(element.itertext())))


def _build_graph(root: ET.Element) -> tuple[nx.DiGraph, dict[str, ET.Element]]:
    schema = load_schema_metadata()
    graph = nx.DiGraph()
    lookup: dict[str, ET.Element] = {}

    def walk(element: ET.Element, path: str, parent_id: Optional[str] = None) -> None:
        node_id = _element_id(element, path)
        lookup[node_id] = element

        attributes = {key: _normalize_text(value) for key, value in element.attrib.items()}
        status_fields = _extract_status_fields(element, schema)
        node_type = _schema_type_name(element)

        graph.add_node(
            node_id,
            tag=_local_name(element.tag),
            type=node_type,
            title=_extract_title(element),
            annotation=_extract_annotation(element),
            text=_strip_html(_normalize_text(" ".join(element.itertext()))),
            attributes=attributes,
            status_fields=status_fields,
            path=path,
        )

        if parent_id is not None:
            graph.add_edge(parent_id, node_id, relation="contains")

        for attr_name, attr_value in attributes.items():
            lowered = attr_name.lower()
            if lowered in RELATION_ATTRS or lowered.endswith("ref") or lowered.endswith("refs"):
                for ref in _split_refs(attr_value):
                    if ref and ref != node_id:
                        existing = graph.get_edge_data(node_id, ref, default={})
                        if existing.get("edge_kind") == "link":
                            continue
                        graph.add_edge(node_id, ref, relation=attr_name, edge_kind="reference")

        if _local_name(element.tag).lower() == "link":
            source_ref, target_ref = _link_endpoints(element)
            if source_ref and target_ref and source_ref in graph and target_ref in graph:
                link_type_code = _normalize_text(element.findtext("type") or element.attrib.get("type"))
                graph.add_edge(
                    source_ref,
                    target_ref,
                    relation=_link_type_metadata(link_type_code).get("key", "link"),
                    edge_kind="link",
                    link_type_code=link_type_code,
                    link_reference=_normalize_text(element.attrib.get("reference")),
                )

        for index, child in enumerate(list(element), start=1):
            child_path = f"{path}/{_local_name(child.tag)}[{index}]"
            walk(child, child_path, node_id)

    walk(root, f"/{_local_name(root.tag)}[1]")
    return graph, lookup


def _graph_payload(graph: nx.DiGraph) -> dict[str, Any]:
    nodes = []
    for node_id, data in graph.nodes(data=True):
        nodes.append(
            {
                "id": node_id,
                "tag": data.get("tag"),
                "type": data.get("type"),
                "title": data.get("title"),
                "annotation": data.get("annotation"),
                "text": data.get("text"),
                "attributes": data.get("attributes", {}),
                "status_fields": data.get("status_fields", {}),
                "path": data.get("path"),
            }
        )

    edges = []
    for source, target, data in graph.edges(data=True):
        edges.append(
            {
                "source": source,
                "target": target,
                "relation": data.get("relation"),
                "edge_kind": data.get("edge_kind"),
            }
        )

    return {"nodes": nodes, "edges": edges}


def _clone_element(element: ET.Element) -> ET.Element:
    return ET.fromstring(ET.tostring(element, encoding="utf-8"))


def _clone_tree(root: ET.Element) -> ET.Element:
    return _clone_element(root)


def _link_type_code(link_type_key: str) -> str:
    schema = load_schema_metadata()
    keys = list(schema.get("link_types", {}).keys())
    normalized = _normalize_text(link_type_key)
    if normalized in schema.get("link_types", {}):
        return str(keys.index(normalized) + 1)
    return "1"


def _unique_link_reference(existing_ids: set[str], source_reference: str, destination_reference: str, relation: str) -> str:
    base = f"LN{source_reference}{destination_reference}"
    candidate = base
    counter = 1
    while candidate in existing_ids:
        candidate = f"{base}-{counter}"
        counter += 1
    return candidate


def _iter_link_edges(graph: nx.DiGraph) -> list[tuple[str, str, dict[str, Any]]]:
    edges: list[tuple[str, str, dict[str, Any]]] = []
    for source, target, data in graph.edges(data=True):
        if data.get("edge_kind") == "link":
            edges.append((source, target, dict(data)))
    edges.sort(key=lambda item: (item[0], item[1], _normalize_text(item[2].get("relation"))))
    return edges


def _sync_graph_node_to_element(element: ET.Element, node_id: str, data: dict[str, Any], schema: dict[str, Any]) -> None:
    node_type = _normalize_text(data.get("type"))
    if node_type and node_type not in schema.get("node_types", {}):
        raise ValueError(f"Unknown schema node type: {node_type}")

    element.set("reference", node_id)

    title = _normalize_text(data.get("title"))
    if title:
        _update_primary_text(element, title)

    annotation = _normalize_text(data.get("annotation"))
    if annotation:
        _update_text_node(element, ANNOTATION_TAGS, annotation)

    status_fields = data.get("status_fields") or {}
    unknown = [key for key in status_fields if key not in schema.get("status_fields", {})]
    if unknown:
        raise ValueError(f"Unknown schema status field(s): {', '.join(sorted(unknown))}")
    if status_fields:
        _update_status_fields(element, status_fields)


def _rebuild_links(root: ET.Element, graph: nx.DiGraph) -> int:
    links_container = root.find("links")
    if links_container is None:
        links_container = ET.SubElement(root, "links")

    for child in list(links_container):
        links_container.remove(child)

    existing_ids = _existing_ids(root, "link")
    count = 0
    for source, target, data in _iter_link_edges(graph):
        relation = _normalize_text(data.get("relation"))
        link = ET.SubElement(links_container, "link")
        link_reference = data.get("link_reference") or _unique_link_reference(existing_ids, source, target, relation)
        existing_ids.add(link_reference)
        link.set("reference", link_reference)

        type_element = ET.SubElement(link, "type")
        type_element.text = data.get("link_type_code") or _link_type_code(relation)

        strength_element = ET.SubElement(link, "strength")
        strength_element.text = "1"

        source_element = ET.SubElement(link, "source-reference")
        source_element.text = source

        destination_element = ET.SubElement(link, "destination-reference")
        destination_element.text = target

        attachment = ET.SubElement(link, "attachment")
        attachment.set("x-source", "0")
        attachment.set("y-source", "0")
        attachment.set("x-destination", "0")
        attachment.set("y-destination", "0")
        count += 1

    return count


def _validate_reconstructed_case(graph: nx.DiGraph, root: ET.Element) -> None:
    schema = load_schema_metadata()
    node_ids = {node_id for node_id, data in graph.nodes(data=True) if data.get("tag") == "node"}

    for node_id, data in graph.nodes(data=True):
        if data.get("tag") != "node":
            continue
        node_type = _normalize_text(data.get("type"))
        if node_type and node_type not in schema.get("node_types", {}):
            raise ValueError(f"Unknown schema node type: {node_type}")

        unknown = [key for key in (data.get("status_fields") or {}) if key not in schema.get("status_fields", {})]
        if unknown:
            raise ValueError(f"Unknown schema status field(s): {', '.join(sorted(unknown))}")

    for source, target, data in graph.edges(data=True):
        if data.get("edge_kind") != "link":
            continue
        if source not in node_ids or target not in node_ids:
            raise ValueError(f"Invalid reconstructed link endpoint(s): {source} -> {target}")

    if root.find("nodes") is None:
        raise ValueError("Reconstructed output is missing a nodes container")
    if root.find("links") is None:
        raise ValueError("Reconstructed output is missing a links container")


def _reconstruct_assurance_case_tree(file_path: str) -> tuple[ET.ElementTree, ET.Element, nx.DiGraph]:
    tree, root = _load_tree(file_path)
    graph, lookup = _build_graph(root)

    reconstructed_root = _clone_tree(root)
    for node_id, data in graph.nodes(data=True):
        if data.get("tag") != "node":
            continue
        element = _find_element(reconstructed_root, node_id)
        if element is None:
            continue
        _sync_graph_node_to_element(element, node_id, data, load_schema_metadata())

    _rebuild_links(reconstructed_root, graph)
    _validate_reconstructed_case(graph, reconstructed_root)

    return ET.ElementTree(reconstructed_root), reconstructed_root, graph


def _default_reconstructed_path(source_path: str | Path) -> Path:
    source = Path(source_path)
    candidate = source.with_name(f"{source.stem}.reconstructed{source.suffix}")
    counter = 1
    while candidate.exists():
        candidate = source.with_name(f"{source.stem}.reconstructed-{counter}{source.suffix}")
        counter += 1
    return candidate


def _resolve_output_path(source_path: str | Path, output_path: str | None = None) -> Path:
    if output_path:
        candidate = Path(output_path).expanduser()
        if not candidate.is_absolute():
            candidate = Path(source_path).parent / candidate
        return candidate
    return _default_reconstructed_path(source_path)


def _existing_ids(root: ET.Element, tag_name: str, attribute_name: str = "reference") -> set[str]:
    values: set[str] = set()
    for element in root.findall(f".//{tag_name}"):
        value = _normalize_text(element.attrib.get(attribute_name))
        if value:
            values.add(value)
    return values


def _allocate_numeric_reference(existing_ids: set[str], prefix: str) -> str:
    highest = 0
    for value in existing_ids:
        if value.startswith(prefix):
            suffix = value[len(prefix) :]
            if suffix.isdigit():
                highest = max(highest, int(suffix))

    candidate = f"{prefix}{highest + 1}"
    while candidate in existing_ids:
        highest += 1
        candidate = f"{prefix}{highest + 1}"
    return candidate


def _layout_offsets(node: ET.Element, dx: int = 4000, dy: int = 0) -> dict[str, str]:
    layout = node.find("layout")
    if layout is None:
        return {"x": str(dx), "y": str(dy), "height": "3960", "width": "3960"}

    attributes = {key: value for key, value in layout.attrib.items()}
    x_value = _normalize_text(attributes.get("x"))
    y_value = _normalize_text(attributes.get("y"))

    try:
        attributes["x"] = str(int(x_value) + dx)
    except ValueError:
        attributes["x"] = str(dx)

    try:
        attributes["y"] = str(int(y_value) + dy)
    except ValueError:
        attributes["y"] = str(dy)

    attributes.setdefault("height", "3960")
    attributes.setdefault("width", "3960")
    return attributes


def _ensure_status_field(container: ET.Element, name: str, value: str) -> None:
    for child in list(container):
        key = _normalize_text(child.attrib.get("name") or child.attrib.get("key") or child.findtext("key")).lower()
        if key == name.lower():
            child.text = value
            return

    status_field = ET.SubElement(container, "status-field")
    status_field.set("name", name)
    status_field.set("type", "string")
    status_field.text = value


def _update_primary_text(element: ET.Element, text: str) -> bool:
    normalized = _normalize_text(text)
    updated = False

    for candidate in TITLE_TAGS:
        for child in list(element):
            if _local_name(child.tag).lower() == candidate:
                child.text = normalized
                updated = True
                break
        if updated:
            break

    if not updated:
        created = ET.SubElement(element, TITLE_TAGS[0])
        created.text = normalized

    if "title" in element.attrib:
        element.set("title", normalized)
    if "name" in element.attrib:
        element.set("name", normalized)
    if "label" in element.attrib:
        element.set("label", normalized)

    return True


def _ensure_views_include(
    root: ET.Element,
    node_reference: str,
    layout_attrs: dict[str, str],
    target_reference: str | None = None,
) -> None:
    views_container = root.find("views")
    if views_container is None:
        return

    for view in views_container.findall("view"):
        nodes_container = view.find("nodes")
        if nodes_container is None:
            nodes_container = ET.SubElement(view, "nodes")

        if target_reference is not None and not any(
            _normalize_text(node.attrib.get("reference")) == target_reference for node in nodes_container.findall("node")
        ):
            continue

        if any(_normalize_text(node.attrib.get("reference")) == node_reference for node in nodes_container.findall("node")):
            continue

        view_node = ET.SubElement(nodes_container, "node")
        view_node.set("reference", node_reference)
        layout = ET.SubElement(view_node, "layout")
        for key, value in layout_attrs.items():
            layout.set(key, value)


def _ensure_link_exists(root: ET.Element, reference: str, link_type: str, source_reference: str, destination_reference: str) -> ET.Element:
    links_container = root.find("links")
    if links_container is None:
        links_container = ET.SubElement(root, "links")

    existing = { _normalize_text(link.attrib.get("reference")) for link in links_container.findall("link") }
    candidate = reference
    counter = 1
    while candidate in existing:
        candidate = f"{reference}-{counter}"
        counter += 1

    link = ET.SubElement(links_container, "link")
    link.set("reference", candidate)
    link_type_el = ET.SubElement(link, "type")
    link_type_el.text = link_type
    strength_el = ET.SubElement(link, "strength")
    strength_el.text = "1"
    source_el = ET.SubElement(link, "source-reference")
    source_el.text = source_reference
    dest_el = ET.SubElement(link, "destination-reference")
    dest_el.text = destination_reference
    attachment = ET.SubElement(link, "attachment")
    attachment.set("x-source", "0")
    attachment.set("y-source", "0")
    attachment.set("x-destination", "0")
    attachment.set("y-destination", "0")
    return link


def _node_payload(node_id: str, data: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": node_id,
        "tag": data.get("tag"),
        "type": data.get("type"),
        "title": data.get("title"),
        "annotation": data.get("annotation"),
        "text": data.get("text"),
        "attributes": data.get("attributes", {}),
        "status_fields": data.get("status_fields", {}),
        "path": data.get("path"),
    }


def _link_endpoints(link: ET.Element) -> tuple[str, str]:
    source = _normalize_text(
        link.findtext("source-reference")
        or link.findtext("source")
        or link.findtext("from")
        or link.attrib.get("source-reference")
        or link.attrib.get("source")
        or link.attrib.get("from")
    )
    target = _normalize_text(
        link.findtext("destination-reference")
        or link.findtext("destination")
        or link.findtext("target")
        or link.attrib.get("destination-reference")
        or link.attrib.get("destination")
        or link.attrib.get("target")
    )
    return source, target


def _link_type_metadata(link_type_code: str) -> dict[str, str]:
    schema = load_schema_metadata()
    link_types = list(schema.get("link_types", {}).items())
    metadata: dict[str, str] = {"code": link_type_code, "key": "unknown"}

    if link_type_code.isdigit():
        index = int(link_type_code) - 1
        if 0 <= index < len(link_types):
            metadata["key"] = link_types[index][0]
            metadata.update(link_types[index][1])
            return metadata

    if link_type_code in schema.get("link_types", {}):
        metadata["key"] = link_type_code
        metadata.update(schema["link_types"][link_type_code])

    return metadata


def _semantic_link_targets(root: ET.Element) -> set[str]:
    targets: set[str] = set()
    for link in root.findall(".//link"):
        _, target = _link_endpoints(link)
        if target:
            targets.add(target)
    return targets


def _load_tree(file_path: str | Path) -> tuple[ET.ElementTree, ET.Element]:
    tree = ET.parse(str(file_path))
    return tree, tree.getroot()


def _find_element(root: ET.Element, node_id: str) -> Optional[ET.Element]:
    direct = root.find(f"./nodes/node[@reference='{node_id}']")
    if direct is not None:
        return direct

    for node in root.findall("./nodes/node"):
        if _normalize_text(node.attrib.get("reference")) == node_id:
            return node

    _, lookup = _build_graph(root)
    return lookup.get(node_id)


def _bootstrap_case_root(case_title: str | None = None) -> ET.Element:
    root = ET.Element("asce")
    if case_title:
        title = ET.SubElement(root, "title")
        title.text = _normalize_text(case_title)

    ET.SubElement(root, "nodes")
    ET.SubElement(root, "links")

    return root


def _bootstrap_destination_path(output_path: str | None) -> Path:
    if output_path:
        candidate = Path(output_path).expanduser()
        if not candidate.is_absolute():
            candidate = Path.cwd() / candidate
        return candidate
    return Path.cwd() / "bootstrap-case.axml"


def _bootstrap_default_strategy(pattern_name: str | None = None) -> str:
    if not pattern_name:
        return "hybrid"
    lowered = pattern_name.lower()
    if "security" in lowered:
        return "threat-oriented"
    if "safety" in lowered:
        return "risk-oriented"
    return "hybrid"


def _bootstrap_node_attrs(role: str, extra: dict[str, Any] | None = None) -> dict[str, Any]:
    attrs = {"bootstrap-role": role}
    if extra:
        attrs.update({str(key): _normalize_text(value) for key, value in extra.items()})
    return attrs


def _bootstrap_node_defaults(role: str) -> tuple[str, str]:
    role = _normalize_text(role).lower()
    if role in {"strategy"}:
        return "argument", "supports"
    if role in {"context", "assumption"}:
        return "comment", "commentson"
    if role in {"evidence-placeholder", "evidence-gap"}:
        return "evidence", "isevidencefor"
    if role in {"defeater"}:
        return "defeater", "defeats"
    return "other", "supports"


def _bootstrap_parent_for_layout(root: ET.Element, parent_node_id: str | None) -> ET.Element | None:
    if not parent_node_id:
        return None
    return _find_element(root, parent_node_id)


def _append_bootstrap_node(
    root: ET.Element,
    *,
    title: str,
    annotation: str | None = None,
    role: str = "context",
    node_type: str | None = None,
    status_fields: dict[str, Any] | None = None,
    attributes: dict[str, Any] | None = None,
    parent_node_id: str | None = None,
    link_type: str | None = None,
) -> tuple[str, str | None]:
    nodes_container = root.find("nodes")
    if nodes_container is None:
        nodes_container = ET.SubElement(root, "nodes")

    existing_ids = _existing_ids(root, "node")
    node_id = _allocate_numeric_reference(existing_ids, "N")
    resolved_type, default_link_type = _bootstrap_node_defaults(role)
    resolved_type = _schema_node_type_key(node_type or resolved_type)
    link_type_key = _normalize_text(link_type) or default_link_type

    node = ET.SubElement(nodes_container, "node")
    node.set("reference", node_id)
    node_type_el = ET.SubElement(node, "type")
    node_type_el.text = _schema_node_type_code(resolved_type)
    user_id = ET.SubElement(node, "user-id")
    user_id.text = node_id
    user_title = ET.SubElement(node, "user-title")
    user_title.text = _normalize_text(title)
    html_annotation = ET.SubElement(node, "html-annotation")
    html_annotation.text = _normalize_text(annotation or title)

    layout = ET.SubElement(node, "layout")
    parent_element = _bootstrap_parent_for_layout(root, parent_node_id)
    layout_source = parent_element if parent_element is not None else node
    layout_attrs = _layout_offsets(layout_source, dx=4000, dy=0)
    for key, value in layout_attrs.items():
        layout.set(key, value)

    status_container = ET.SubElement(node, "status-fields")
    _ensure_status_field(status_container, "annotation", _normalize_text(annotation or title))
    _ensure_status_field(status_container, "confidence", _normalize_text((status_fields or {}).get("confidence", "low" if role in {"evidence-placeholder", "assumption"} else "medium")))
    if status_fields:
        for key, value in status_fields.items():
            if key in {"annotation", "confidence"}:
                continue
            _ensure_status_field(status_container, str(key), _normalize_text(value))

    node.set("bootstrap-role", _normalize_text(role))
    if attributes:
        for key, value in attributes.items():
            node.set(str(key), _normalize_text(value))

    _ensure_views_include(root, node_id, layout_attrs, parent_node_id)

    created_link_reference: str | None = None
    if parent_node_id:
        link_reference = _unique_link_reference(_existing_ids(root, "link"), parent_node_id, node_id, link_type_key)
        link = _ensure_link_exists(root, link_reference, _link_type_code(link_type_key), parent_node_id, node_id)
        created_link_reference = _normalize_text(link.attrib.get("reference"))

    return node_id, created_link_reference


def _bootstrap_case_summary(graph: nx.DiGraph, root_claims: list[dict[str, Any]], gaps: list[dict[str, Any]]) -> str:
    claim_titles = ", ".join(item.get("title") or item.get("id") for item in root_claims[:3]) or "none"
    gap_count = len(gaps)
    defeater_count = sum(1 for _, data in graph.nodes(data=True) if _normalize_text(data.get("type")) == "defeater")
    evidence_count = sum(1 for _, data in graph.nodes(data=True) if _normalize_text(data.get("type")) == "evidence")
    return (
        f"Bootstrap summary: {len(root_claims)} root claim(s), {evidence_count} evidence node(s), "
        f"{defeater_count} defeater node(s), and {gap_count} unresolved gap(s). "
        f"Primary roots: {claim_titles}."
    )


def _find_unresolved_gaps(graph: nx.DiGraph) -> list[dict[str, Any]]:
    gaps: list[dict[str, Any]] = []
    for node_id, data in graph.nodes(data=True):
        if data.get("tag") != "node":
            continue

        attributes = data.get("attributes", {}) or {}
        role = _normalize_text(attributes.get("bootstrap-role") or attributes.get("bootstrap_role") or data.get("bootstrap-role"))
        title = _normalize_text(data.get("title"))
        children = list(graph.successors(node_id))

        if role in {"evidence-placeholder", "gap"}:
            gaps.append({"id": node_id, "title": title, "reason": f"bootstrap role is {role}"})
            continue

        if _normalize_text(data.get("type")) in {"claim", "argument"} and not children:
            gaps.append({"id": node_id, "title": title, "reason": "unsupported branch"})

    return gaps


def _materialize_pattern_branch(
    root: ET.Element,
    branch_spec: dict[str, Any],
    *,
    system_name: str,
    system_context: str,
    strategy: str,
    parent_node_id: str | None = None,
) -> list[str]:
    attributes = dict(branch_spec.get("attributes", {}) or {})
    role = _normalize_text(branch_spec.get("role") or attributes.get("bootstrap-role") or branch_spec.get("node_type"))
    node_id, _ = _append_bootstrap_node(
        root,
        title=_normalize_text(branch_spec.get("title", "")),
        annotation=_normalize_text(branch_spec.get("annotation", "")),
        role=role or _schema_node_type_key(branch_spec.get("node_type", "other")),
        node_type=_normalize_text(branch_spec.get("node_type", "other")),
        status_fields={
            "annotation": _normalize_text(branch_spec.get("annotation", "")),
            "confidence": _normalize_text(branch_spec.get("status_fields", {}).get("confidence", "low" if role in {"context", "assumption", "evidence-placeholder"} else "medium")),
            **{str(key): value for key, value in (branch_spec.get("status_fields", {}) or {}).items() if key not in {"annotation", "confidence"}},
        },
        attributes=attributes,
        parent_node_id=parent_node_id,
        link_type=_normalize_text(branch_spec.get("link_type", "")) or None,
    )

    created = [node_id]
    for child in branch_spec.get("children", []) or []:
        created.extend(
            _materialize_pattern_branch(
                root,
                child,
                system_name=system_name,
                system_context=system_context,
                strategy=strategy,
                parent_node_id=node_id,
            )
        )

    return created


@mcp.tool()
def get_node_children(parent_node_id: str, file_path: str | None = None) -> dict[str, Any]:
    """Return the immediate children connected to a node."""
    file_path = _resolve_file_path(file_path)
    _, root = _load_tree(file_path)
    graph, _ = _build_graph(root)

    if parent_node_id not in graph:
        raise ValueError(f"Unknown node_id: {parent_node_id}")

    children: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()

    for link in root.findall(".//link"):
        source, target = _link_endpoints(link)
        if source != parent_node_id or not target:
            continue

        if target not in graph:
            continue

        node_data = graph.nodes[target]
        if node_data.get("tag") != "node":
            continue

        link_type_code = _normalize_text(link.findtext("type") or link.attrib.get("type"))
        link_type = _link_type_metadata(link_type_code)
        key = (target, link_type_code)
        if key in seen:
            continue
        seen.add(key)

        child_payload = _node_payload(target, node_data)
        child_payload["link_type"] = link_type.get("key", "unknown")
        child_payload["link_type_code"] = link_type_code or None
        child_payload["link_reference"] = _normalize_text(link.attrib.get("reference")) or None
        children.append(child_payload)

    return {
        "parent_node_id": parent_node_id,
        "children": children,
    }


@mcp.tool()
def get_root_claims(file_path: str | None = None) -> dict[str, Any]:
    """Return the top-level claims that can serve as traversal entry points."""
    file_path = _resolve_file_path(file_path)
    _, root = _load_tree(file_path)
    graph, _ = _build_graph(root)
    destination_ids = _semantic_link_targets(root)

    roots: list[dict[str, Any]] = []
    for node_id, data in graph.nodes(data=True):
        if data.get("tag") != "node":
            continue
        if data.get("type") not in {"claim", "side-claim", "subcase"}:
            continue
        if node_id in destination_ids:
            continue
        roots.append(_node_payload(node_id, data))

    roots.sort(key=lambda item: (item.get("title") or "", item.get("id") or ""))

    return {
        "file_path": str(file_path),
        "root_claims": roots,
        "count": len(roots),
    }


@mcp.tool()
def reconstruct_assurance_case(file_path: str | None = None, output_path: str | None = None) -> dict[str, Any]:
    """Rebuild an assurance case into a new `.axml` file and promote it to active state."""
    source_path = _resolve_file_path(file_path)
    tree, root, graph = _reconstruct_assurance_case_tree(source_path)
    destination = _resolve_output_path(source_path, output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    tree.write(str(destination), encoding="utf-8", xml_declaration=True)
    active_path = _remember_active_axml_path(destination)
    SHARED_AGENT_CONTEXT["active_case_path"] = active_path

    return {
        "source_file_path": source_path,
        "file_path": active_path,
        "status": "written",
        "node_count": sum(1 for _, data in graph.nodes(data=True) if data.get("tag") == "node"),
        "link_count": len(_iter_link_edges(graph)),
    }


def _update_text_node(element: ET.Element, candidates: tuple[str, ...], value: str) -> bool:
    for candidate in candidates:
        for child in list(element):
            if _local_name(child.tag).lower() == candidate:
                child.text = value
                return True

    for candidate in candidates:
        if candidate in element.attrib:
            element.set(candidate, value)
            return True

    created = ET.SubElement(element, candidates[0])
    created.text = value
    return True


def _update_status_fields(element: ET.Element, status_fields: dict[str, Any]) -> None:
    container = None
    for child in list(element):
        if _local_name(child.tag).lower() in {"status-fields", "statusfield", "status-field"}:
            container = child
            break

    if container is None:
        container = ET.SubElement(element, "status-fields")

    existing: dict[str, ET.Element] = {}
    for child in list(container):
        key = _normalize_text(
            child.attrib.get("name")
            or child.attrib.get("key")
            or child.findtext("key")
        )
        if key:
            existing[key] = child

    for key, value in status_fields.items():
        text = _normalize_text(value)
        if key in existing:
            existing[key].text = text
            continue

        status_field = ET.SubElement(container, "status-field")
        status_field.set("name", str(key))
        status_field.text = text


def _input_hash(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _provenance_lines(fingerprint: str, model_used: str, input_hash: str) -> list[str]:
    return [
        f"MCP Fingerprint: {fingerprint}",
        f"Model: {model_used}",
        f"Timestamp: {datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')}",
        f"Input Hash: sha256:{input_hash}",
    ]


def _strip_existing_provenance(existing_value: str) -> str:
    existing_value = _normalize_text(existing_value)
    if not existing_value:
        return ""

    prefixes = ("MCP Fingerprint:", "Model:", "Timestamp:", "Input Hash:")
    kept_lines = []
    for line in existing_value.splitlines():
        if line.strip().startswith(prefixes):
            break
        kept_lines.append(line)

    return "\n".join(kept_lines).strip()


def _annotation_field_value(existing_value: str, fingerprint: str, model_used: str, input_hash: str) -> str:
    base_value = _strip_existing_provenance(existing_value)
    provenance = "\n".join(_provenance_lines(fingerprint, model_used, input_hash))
    if not base_value:
        return provenance
    return f"{base_value}\n{provenance}"


def _append_annotation_provenance(
    element: ET.Element,
    fingerprint: str,
    model_used: str,
    input_hash: str,
) -> None:
    schema = load_schema_metadata()
    container = None

    for child in list(element):
        if _local_name(child.tag).lower() in {"status-fields", "statusfield", "status-field"}:
            container = child
            break

    if container is None:
        container = ET.SubElement(element, "status-fields")

    annotation_field = None
    for child in list(container):
        key = _normalize_text(
            child.attrib.get("name")
            or child.attrib.get("key")
            or child.findtext("key")
        ).lower()
        if key == "annotation":
            annotation_field = child
            break

    if annotation_field is None:
        annotation_field = ET.SubElement(container, "status-field")
        annotation_field.set("name", "annotation")
        annotation_field.set("type", "string")

    current_value = _normalize_text(annotation_field.text)
    annotation_field.text = _annotation_field_value(current_value, fingerprint, model_used, input_hash)

    # Ensure schema-defined annotation metadata stays discoverable if the file already uses it.
    if "annotation" in schema.get("status_fields", {}):
        annotation_field.set("name", "annotation")
        annotation_field.set("type", annotation_field.attrib.get("type", "string"))


@mcp.tool()
def parse_assurance_case(file_path: str | None = None, focus_node_id: str | None = None, radius: int = 2) -> dict[str, Any]:
    """Parse an AXML assurance case into a schema-aware NetworkX graph."""
    file_path = _resolve_file_path(file_path)
    _, root = _load_tree(file_path)
    graph, _ = _build_graph(root)

    payload: dict[str, Any] = {
        "file_path": str(file_path),
        "schema": load_schema_metadata(),
        "node_count": graph.number_of_nodes(),
        "edge_count": graph.number_of_edges(),
        "graph": _graph_payload(graph),
    }

    if focus_node_id:
        payload["neighborhood"] = get_assurance_neighborhood(focus_node_id, radius, file_path=file_path)

    return payload


@mcp.tool()
def get_assurance_neighborhood(node_id: str, radius: int = 2, file_path: str | None = None) -> dict[str, Any]:
    """Return a local subgraph around a node so subagents can see neighborhood context."""
    file_path = _resolve_file_path(file_path)
    _, root = _load_tree(file_path)
    graph, _ = _build_graph(root)

    if node_id not in graph:
        raise ValueError(f"Unknown node_id: {node_id}")

    radius = max(0, int(radius))
    undirected = graph.to_undirected()
    nodes_in_scope = set(nx.single_source_shortest_path_length(undirected, node_id, cutoff=radius).keys())
    subgraph = graph.subgraph(nodes_in_scope).copy()

    return {
        "center": node_id,
        "radius": radius,
        "schema": load_schema_metadata(),
        "graph": _graph_payload(subgraph),
    }


@mcp.tool()
def set_system_context(brief_text: str) -> str:
    """Save the current system context brief in memory."""
    SHARED_AGENT_CONTEXT["system_brief"] = _normalize_text(brief_text)
    return "Context updated successfully."


@mcp.tool()
def get_system_context() -> str:
    """Retrieve the current system context brief."""
    return SHARED_AGENT_CONTEXT["system_brief"]


@mcp.tool()
def discover_evidence_providers(query: str | None = None, capability: str | None = None) -> dict[str, Any]:
    """Discover available evidence providers using the local registry."""
    providers = [
        provider
        for provider in EVIDENCE_PROVIDER_REGISTRY.values()
        if _provider_matches(provider, query=query, capability=capability)
    ]

    return {
        "query": _normalize_text(query),
        "capability": _normalize_text(capability),
        "count": len(providers),
        "providers": providers,
    }


@mcp.tool()
def list_evidence_providers() -> dict[str, Any]:
    """List all evidence providers in the registry."""
    return discover_evidence_providers()


@mcp.tool()
def get_evidence_provider(name: str) -> dict[str, Any]:
    """Return metadata for one evidence provider."""
    provider = EVIDENCE_PROVIDER_REGISTRY.get(_normalize_text(name))
    if provider is None:
        raise ValueError(f"Unknown evidence provider: {name}")
    return provider


@mcp.tool()
def list_bootstrap_patterns() -> list[dict[str, str]]:
    """List the available bootstrap templates."""
    return _list_bootstrap_patterns()


@mcp.tool()
def get_bootstrap_pattern(name: str) -> dict[str, Any]:
    """Return one bootstrap template by name."""
    return _get_bootstrap_pattern(name)


@mcp.tool()
def create_assurance_case(
    output_path: str | None = None,
    title: str | None = None,
    template_name: str | None = None,
    system_name: str | None = None,
    system_context: str | None = None,
    strategy: str | None = None,
) -> dict[str, Any]:
    """Create a fresh assurance case scaffold and optionally seed it from a bootstrap template."""
    destination = _bootstrap_destination_path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    case_title = _normalize_text(title or f"{system_name or 'Bootstrap'} assurance case")
    root = _bootstrap_case_root(case_title)
    tree = ET.ElementTree(root)
    tree.write(str(destination), encoding="utf-8", xml_declaration=True)

    active_path = _remember_active_axml_path(destination)
    SHARED_AGENT_CONTEXT["active_case_path"] = active_path
    if system_context:
        SHARED_AGENT_CONTEXT["system_brief"] = _normalize_text(system_context)

    created_nodes: list[str] = []
    if template_name:
        created_nodes = instantiate_pattern(
            template_name,
            file_path=str(active_path),
            system_name=system_name or case_title,
            system_context=system_context or "No system context provided.",
            strategy=strategy or _bootstrap_default_strategy(template_name),
        )["created_node_ids"]

    return {
        "file_path": active_path,
        "status": "written",
        "template_name": template_name,
        "created_node_ids": created_nodes,
    }


def _create_bootstrap_node_tool(
    *,
    file_path: str | None,
    title: str,
    annotation: str | None = None,
    role: str,
    node_type: str | None = None,
    parent_node_id: str | None = None,
    link_type: str | None = None,
    status_fields: dict[str, Any] | None = None,
    attributes: dict[str, Any] | None = None,
) -> dict[str, Any]:
    file_path = _resolve_file_path(file_path)
    create_backup(file_path)
    tree, root = _load_tree(file_path)
    graph, _ = _build_graph(root)

    if parent_node_id is not None and parent_node_id not in graph:
        raise ValueError(f"Unknown node_id: {parent_node_id}")

    node_id, link_reference = _append_bootstrap_node(
        root,
        title=title,
        annotation=annotation,
        role=role,
        node_type=node_type,
        status_fields=status_fields,
        attributes=attributes,
        parent_node_id=parent_node_id,
        link_type=link_type,
    )
    tree.write(str(file_path), encoding="utf-8", xml_declaration=True)

    return {
        "file_path": str(file_path),
        "status": "written",
        "node_id": node_id,
        "link_reference": link_reference,
        "node_type": _schema_node_type_key(node_type or _bootstrap_node_defaults(role)[0]),
        "role": role,
    }


@mcp.tool()
def create_claim(
    title: str,
    annotation: str | None = None,
    file_path: str | None = None,
    parent_node_id: str | None = None,
    link_type: str | None = "supports",
    status_fields: dict[str, Any] | None = None,
    attributes: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return _create_bootstrap_node_tool(
        file_path=file_path,
        title=title,
        annotation=annotation,
        role="claim",
        node_type="claim",
        parent_node_id=parent_node_id,
        link_type=link_type,
        status_fields=status_fields,
        attributes=attributes,
    )


@mcp.tool()
def create_context(
    title: str,
    annotation: str | None = None,
    file_path: str | None = None,
    parent_node_id: str | None = None,
    link_type: str | None = "commentson",
    status_fields: dict[str, Any] | None = None,
    attributes: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return _create_bootstrap_node_tool(
        file_path=file_path,
        title=title,
        annotation=annotation,
        role="context",
        node_type="comment",
        parent_node_id=parent_node_id,
        link_type=link_type,
        status_fields=status_fields,
        attributes=attributes,
    )


@mcp.tool()
def create_assumption(
    title: str,
    annotation: str | None = None,
    file_path: str | None = None,
    parent_node_id: str | None = None,
    link_type: str | None = "commentson",
    status_fields: dict[str, Any] | None = None,
    attributes: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return _create_bootstrap_node_tool(
        file_path=file_path,
        title=title,
        annotation=annotation,
        role="assumption",
        node_type="comment",
        parent_node_id=parent_node_id,
        link_type=link_type,
        status_fields=status_fields,
        attributes=attributes,
    )


@mcp.tool()
def create_evidence_placeholder(
    title: str,
    annotation: str | None = None,
    file_path: str | None = None,
    parent_node_id: str | None = None,
    link_type: str | None = "isevidencefor",
    status_fields: dict[str, Any] | None = None,
    attributes: dict[str, Any] | None = None,
) -> dict[str, Any]:
    merged_status_fields = {"confidence": "low"}
    if status_fields:
        merged_status_fields.update(status_fields)
    merged_attributes = {"bootstrap-placeholder": "true"}
    if attributes:
        merged_attributes.update(attributes)
    return _create_bootstrap_node_tool(
        file_path=file_path,
        title=title,
        annotation=annotation,
        role="evidence-placeholder",
        node_type="evidence",
        parent_node_id=parent_node_id,
        link_type=link_type,
        status_fields=merged_status_fields,
        attributes=merged_attributes,
    )


@mcp.tool()
def create_defeater(
    title: str,
    annotation: str | None = None,
    file_path: str | None = None,
    parent_node_id: str | None = None,
    link_type: str | None = "defeats",
    status_fields: dict[str, Any] | None = None,
    attributes: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return _create_bootstrap_node_tool(
        file_path=file_path,
        title=title,
        annotation=annotation,
        role="defeater",
        node_type="defeater",
        parent_node_id=parent_node_id,
        link_type=link_type,
        status_fields=status_fields,
        attributes=attributes,
    )


@mcp.tool()
def create_link(
    source_node_id: str,
    target_node_id: str,
    link_type: str = "supports",
    file_path: str | None = None,
) -> dict[str, Any]:
    file_path = _resolve_file_path(file_path)
    create_backup(file_path)
    tree, root = _load_tree(file_path)
    graph, _ = _build_graph(root)

    if source_node_id not in graph:
        raise ValueError(f"Unknown node_id: {source_node_id}")
    if target_node_id not in graph:
        raise ValueError(f"Unknown node_id: {target_node_id}")

    link = _ensure_link_exists(root, _unique_link_reference(_existing_ids(root, "link"), source_node_id, target_node_id, link_type), _link_type_code(link_type), source_node_id, target_node_id)
    tree.write(str(file_path), encoding="utf-8", xml_declaration=True)

    return {
        "file_path": str(file_path),
        "status": "written",
        "link_reference": _normalize_text(link.attrib.get("reference")),
        "source_node_id": source_node_id,
        "target_node_id": target_node_id,
        "link_type": _normalize_text(link_type),
    }


@mcp.tool()
def instantiate_pattern(
    pattern_name: str,
    file_path: str | None = None,
    output_path: str | None = None,
    system_name: str | None = None,
    system_context: str | None = None,
    strategy: str | None = None,
) -> dict[str, Any]:
    destination = _resolve_file_path(file_path or output_path) if (file_path or output_path) else _bootstrap_destination_path(None)
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)

    if not destination.exists():
        root = _bootstrap_case_root(f"{system_name or 'Bootstrap'} assurance case")
        ET.ElementTree(root).write(str(destination), encoding="utf-8", xml_declaration=True)

    create_backup(str(destination))
    tree, root = _load_tree(str(destination))
    graph, _ = _build_graph(root)

    rendered = _render_bootstrap_pattern(
        pattern_name,
        system_name=system_name or "the system",
        system_context=system_context or _normalize_text(get_system_context()),
        strategy=strategy or _bootstrap_default_strategy(pattern_name),
    )
    created_node_ids = _materialize_pattern_branch(
        root,
        rendered["root"],
        system_name=system_name or "the system",
        system_context=system_context or _normalize_text(get_system_context()),
        strategy=strategy or _bootstrap_default_strategy(pattern_name),
    )

    tree.write(str(destination), encoding="utf-8", xml_declaration=True)
    active_path = _remember_active_axml_path(destination)
    SHARED_AGENT_CONTEXT["active_case_path"] = active_path
    if system_context:
        SHARED_AGENT_CONTEXT["system_brief"] = _normalize_text(system_context)

    return {
        "file_path": active_path,
        "status": "written",
        "pattern_name": pattern_name,
        "created_node_ids": created_node_ids,
        "node_count": sum(1 for _, data in graph.nodes(data=True) if data.get("tag") == "node"),
        "link_count": len(_iter_link_edges(graph)),
    }


@mcp.tool()
def find_unresolved_gaps(file_path: str | None = None) -> dict[str, Any]:
    file_path = _resolve_file_path(file_path)
    _, root = _load_tree(file_path)
    graph, _ = _build_graph(root)
    gaps = _find_unresolved_gaps(graph)
    return {
        "file_path": file_path,
        "count": len(gaps),
        "gaps": gaps,
    }


@mcp.tool()
def validate_case_structure(file_path: str | None = None) -> dict[str, Any]:
    file_path = _resolve_file_path(file_path)
    _, root = _load_tree(file_path)
    graph, _ = _build_graph(root)
    schema = load_schema_metadata()

    issues: list[str] = []
    nodes = root.find("nodes")
    links = root.find("links")
    if nodes is None:
        issues.append("missing nodes container")
    if links is None:
        issues.append("missing links container")

    for node_id, data in graph.nodes(data=True):
        if data.get("tag") != "node":
            continue
        node_type = _normalize_text(data.get("type"))
        if node_type and node_type not in schema.get("node_types", {}):
            issues.append(f"unknown node type: {node_type} ({node_id})")
        for key in (data.get("status_fields") or {}):
            if key not in schema.get("status_fields", {}):
                issues.append(f"unknown status field: {key} ({node_id})")

    if not any(_normalize_text(data.get("type")) == "claim" for _, data in graph.nodes(data=True)):
        issues.append("no claim nodes found")

    for source, target, data in graph.edges(data=True):
        if data.get("edge_kind") != "link":
            continue
        if source not in graph or target not in graph:
            issues.append(f"invalid link endpoint: {source} -> {target}")

    return {
        "file_path": file_path,
        "valid": not issues,
        "issues": issues,
        "node_count": sum(1 for _, data in graph.nodes(data=True) if data.get("tag") == "node"),
        "link_count": len(_iter_link_edges(graph)),
    }


@mcp.tool()
def generate_case_summary(file_path: str | None = None) -> dict[str, Any]:
    file_path = _resolve_file_path(file_path)
    _, root = _load_tree(file_path)
    graph, _ = _build_graph(root)
    roots = get_root_claims(file_path=file_path)["root_claims"]
    gaps = _find_unresolved_gaps(graph)
    summary = _bootstrap_case_summary(graph, roots, gaps)
    return {
        "file_path": file_path,
        "summary": summary,
        "root_claims": roots,
        "gaps": gaps,
    }


@mcp.tool()
def write_defeater(
    target_node_id: str,
    title: str | None = None,
    annotation: str | None = None,
    file_path: str | None = None,
) -> dict[str, Any]:
    """Create a defeater node and attach it to a target node."""
    file_path = _resolve_file_path(file_path)
    create_backup(file_path)
    tree, root = _load_tree(file_path)
    graph, _ = _build_graph(root)

    if target_node_id not in graph:
        raise ValueError(f"Unknown node_id: {target_node_id}")

    target_type = _normalize_text(graph.nodes[target_node_id].get("type"))
    if target_type in {"comment", "caption"}:
        raise ValueError(f"Defeaters cannot be attached to {target_type} nodes")

    nodes_container = root.find("nodes")
    if nodes_container is None:
        nodes_container = ET.SubElement(root, "nodes")

    target_element = _find_element(root, target_node_id)
    if target_element is None:
        raise ValueError(f"Unknown node_id: {target_node_id}")

    existing_node_ids = set(graph.nodes)
    defeater_node_id = _allocate_numeric_reference(existing_node_ids, "N")
    defeater_title = _normalize_text(title or annotation or f"Defeater for {target_node_id}")

    defeater_node = ET.SubElement(nodes_container, "node")
    defeater_node.set("reference", defeater_node_id)

    layout = ET.SubElement(defeater_node, "layout")
    for key, value in _layout_offsets(target_element, dx=4000, dy=0).items():
        layout.set(key, value)

    node_type = ET.SubElement(defeater_node, "type")
    node_type.text = "8"

    user_id = ET.SubElement(defeater_node, "user-id")
    user_id.text = defeater_node_id

    user_title = ET.SubElement(defeater_node, "user-title")
    user_title.text = defeater_title

    status_fields = ET.SubElement(defeater_node, "status-fields")
    if annotation is not None:
        _ensure_status_field(status_fields, "annotation", _normalize_text(annotation))
    else:
        _ensure_status_field(status_fields, "annotation", "")

    html_annotation = ET.SubElement(defeater_node, "html-annotation")
    html_annotation.text = _normalize_text(annotation or defeater_title)

    links_container = root.find("links")
    if links_container is None:
        links_container = ET.SubElement(root, "links")

    link_reference = f"LN{defeater_node_id}{target_node_id}"
    link = _ensure_link_exists(root, link_reference, "5", defeater_node_id, target_node_id)

    _ensure_views_include(root, defeater_node_id, _layout_offsets(target_element, dx=4000, dy=0), target_node_id)

    tree.write(str(file_path), encoding="utf-8", xml_declaration=True)

    return {
        "file_path": str(file_path),
        "mutation": "write_defeater",
        "status": "written",
        "target_node_id": target_node_id,
        "defeater_node_id": defeater_node_id,
        "link_reference": _normalize_text(link.attrib.get("reference")),
    }


def _rewrite_node_text(file_path: str | None, node_id: str, text: str) -> dict[str, Any]:
    file_path = _resolve_file_path(file_path)
    create_backup(file_path)
    tree, root = _load_tree(file_path)
    element = _find_element(root, node_id)
    if element is None:
        raise ValueError(f"Unknown node_id: {node_id}")

    _update_primary_text(element, text)
    tree.write(str(file_path), encoding="utf-8", xml_declaration=True)

    return {
        "file_path": str(file_path),
        "mutation": "rewrite_node",
        "status": "written",
        "node_id": node_id,
        "changed_fields": ["title"],
    }


@mcp.tool()
def update_node(node_id: str, text: str, file_path: str | None = None) -> dict[str, Any]:
    """Rewrite the primary text of an existing node in place."""
    return _rewrite_node_text(file_path, node_id, text)


@mcp.tool()
def rewrite_node(node_id: str, text: str, file_path: str | None = None) -> dict[str, Any]:
    """Alias for update_node."""
    return _rewrite_node_text(file_path, node_id, text)


@mcp.tool()
def modify_assurance_case(
    node_id: str,
    title: str | None = None,
    annotation: str | None = None,
    status_fields: dict[str, Any] | None = None,
    attributes: dict[str, Any] | None = None,
    file_path: str | None = None,
) -> dict[str, Any]:
    """Apply targeted updates to an AXML file and persist them in place."""
    file_path = _resolve_file_path(file_path)
    create_backup(file_path)
    schema = load_schema_metadata()
    tree, root = _load_tree(file_path)
    element = _find_element(root, node_id)
    if element is None:
        raise ValueError(f"Unknown node_id: {node_id}")

    changed_fields: list[str] = []

    if title is not None:
        _update_text_node(element, TITLE_TAGS, _normalize_text(title))
        changed_fields.append("title")

    if annotation is not None:
        _update_text_node(element, ANNOTATION_TAGS, _normalize_text(annotation))
        changed_fields.append("annotation")

    if status_fields:
        known_status_fields = schema.get("status_fields", {})
        unknown = [key for key in status_fields if key not in known_status_fields]
        if unknown:
            raise ValueError(f"Unknown schema status field(s): {', '.join(sorted(unknown))}")
        _update_status_fields(element, status_fields)
        changed_fields.append("status_fields")

    if attributes:
        for key, value in attributes.items():
            element.set(str(key), _normalize_text(value))
        changed_fields.append("attributes")

    provenance_input = {
        "file_path": str(file_path),
        "node_id": node_id,
        "title": _normalize_text(title) if title is not None else None,
        "annotation": _normalize_text(annotation) if annotation is not None else None,
        "status_fields": {str(key): _normalize_text(value) for key, value in (status_fields or {}).items()} or None,
        "attributes": {str(key): _normalize_text(value) for key, value in (attributes or {}).items()} or None,
    }
    _append_annotation_provenance(element, MCP_FINGERPRINT, MODEL_USED, _input_hash(provenance_input))
    changed_fields.append("annotation_provenance")

    tree.write(str(file_path), encoding="utf-8", xml_declaration=True)

    return {
        "file_path": str(file_path),
        "node_id": node_id,
        "changed_fields": changed_fields,
        "status": "written",
    }


if __name__ == "__main__":
    mcp.run()
