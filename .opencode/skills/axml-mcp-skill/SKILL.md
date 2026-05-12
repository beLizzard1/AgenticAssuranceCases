---
name: axml-mcp-skill
description: Use the AXML MCP server for assurance-case work. Prefer MCP for structural edits, validation, inspection, and export, and discover tools before assuming exact names.
license: MIT
compatibility: Requires the AXML MCP server and OpenCode.
metadata:
  author: Agentic Assurance Cases
  version: "1.0"
---

# AXML MCP Skill

Use the AXML MCP server to inspect, modify, and route assurance-case work represented in AXML.

## Purpose

This skill gives agents one canonical operating model for assurance-case work. Treat the AXML MCP server as the semantic source of truth for case structure, traceability, validation, and exports.

## When to Use

Use this skill when the user asks to:

- create or update an assurance case
- add, remove, rename, or restructure claims, arguments, evidence, contexts, assumptions, justifications, or defeaters
- check traceability between claims and evidence
- query an assurance-case graph
- manage shared system context for downstream agents
- create defeaters or update targeted node content through MCP write-back tools

Do not use this skill for purely editorial wording changes unless the wording is attached to a formal assurance-case node.

## Core Principle

Treat the AXML MCP server as the source of semantic truth.

Agents may draft proposed changes in natural language or markdown, but structural changes MUST be applied through MCP tools where available. Direct file edits are only acceptable for unsupported metadata, comments, examples, or documentation.

## Workflow

1. Discover the available AXML MCP tools first.
2. Load or inspect the AXML document through MCP.
3. Query the graph, neighborhood, or root claims as needed.
4. Apply structural changes through MCP tools instead of editing raw `.axml` directly.
5. Prefer the reconstructed or canonical output for follow-up interactions when the server provides one.

## Expected MCP Capabilities

Current capabilities in this repository:

- parse assurance cases into a schema-aware graph
- fetch neighborhood context around a node
- list root claims
- list immediate children of a node
- save and retrieve shared system context
- discover, list, and inspect evidence providers
- update existing nodes or apply targeted write-back mutations
- create defeater nodes and defeats links

Recommended capabilities in broader deployments:

- query graph
- find orphaned nodes
- find unsupported claims
- find evidence without consuming claims
- find circular support
- check unresolved defeaters
- check context coverage
- check schema compliance
- generate summary
- generate visualisation
- import from intermediate representation
- diff two assurance cases
- produce machine-readable validation report

## Common Mistakes

- Do not assume the exact MCP tool names without discovery.
- Do not rewrite structural assurance-case content as raw XML when MCP tools are available.
- Do not use this skill for unrelated editorial text.
