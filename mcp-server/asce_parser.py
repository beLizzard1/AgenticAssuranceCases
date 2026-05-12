from __future__ import annotations

from functools import lru_cache
from datetime import datetime, timezone
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any, Optional
import xml.etree.ElementTree as ET

import networkx as nx
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP


REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schemas" / "ASCAD 2.0.xml"

MCP_SERVER_NAME = "asce_tools"
mcp = FastMCP(MCP_SERVER_NAME)
MCP_FINGERPRINT = "asce_parser_v1.0.3_abc123"
MODEL_USED = "gpt-5.4-mini"
SHARED_AGENT_CONTEXT = {"system_brief": "No context provided yet."}
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


register_evidence_provider(
    "asce_tools",
    "Schema-aware ASCE parser, neighborhood, registry, and write-back tools",
    capabilities=[
        "parse_assurance_case",
        "get_assurance_neighborhood",
        "get_root_claims",
        "get_node_children",
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
                        graph.add_edge(node_id, ref, relation=attr_name)

        if _local_name(element.tag).lower() == "link":
            source_ref, target_ref = _link_endpoints(element)
            if source_ref and target_ref and source_ref in graph and target_ref in graph:
                link_type_code = _normalize_text(element.findtext("type") or element.attrib.get("type"))
                graph.add_edge(source_ref, target_ref, relation=_link_type_metadata(link_type_code).get("key", "link"))

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
            }
        )

    return {"nodes": nodes, "edges": edges}


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


@mcp.tool()
def get_node_children(file_path: str, parent_node_id: str) -> dict[str, Any]:
    """Return the immediate children connected to a node."""
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
def get_root_claims(file_path: str) -> dict[str, Any]:
    """Return the top-level claims that can serve as traversal entry points."""
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
def parse_assurance_case(file_path: str, focus_node_id: str | None = None, radius: int = 2) -> dict[str, Any]:
    """Parse an AXML assurance case into a schema-aware NetworkX graph."""
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
        payload["neighborhood"] = get_assurance_neighborhood(file_path, focus_node_id, radius)

    return payload


@mcp.tool()
def get_assurance_neighborhood(file_path: str, node_id: str, radius: int = 2) -> dict[str, Any]:
    """Return a local subgraph around a node so subagents can see neighborhood context."""
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
def write_defeater(
    file_path: str,
    target_node_id: str,
    title: str | None = None,
    annotation: str | None = None,
) -> dict[str, Any]:
    """Create a defeater node and attach it to a target node."""
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


def _rewrite_node_text(file_path: str, node_id: str, text: str) -> dict[str, Any]:
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
def update_node(file_path: str, node_id: str, text: str) -> dict[str, Any]:
    """Rewrite the primary text of an existing node in place."""
    return _rewrite_node_text(file_path, node_id, text)


@mcp.tool()
def rewrite_node(file_path: str, node_id: str, text: str) -> dict[str, Any]:
    """Alias for update_node."""
    return _rewrite_node_text(file_path, node_id, text)


@mcp.tool()
def modify_assurance_case(
    file_path: str,
    node_id: str,
    title: str | None = None,
    annotation: str | None = None,
    status_fields: dict[str, Any] | None = None,
    attributes: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Apply targeted updates to an AXML file and persist them in place."""
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
