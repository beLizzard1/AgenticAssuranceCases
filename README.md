# Agentic Assurance Cases

This repository contains an OpenCode-based environment for evaluating Claim-Argument-Evidence (CAE) assurance cases using the Helping Hand notation. It uses a local Model Context Protocol (MCP) server to parse and inspect Adelard ASCE `.axml` files as structured graphs instead of raw XML.

## Features
* **Assurance Evaluator Agent:** The primary agent that routes claims to the right justification strategy.
* **Top-Down Architect Agent:** A root-first orchestrator that walks the assurance tree downward using targeted MCP navigation tools.
* **Narrative Synthesizer Agent:** A human-facing briefing mode plus a shared system-context generator for downstream agents.
* **Specialized Assurance Subagents:** Evidence Incorporation, Calculation, Decomposition, Substitution, and Concretion.
* **Adversarial Evaluator Agent:** A red-team pass with rebutting, undercutting, and undermining defeater strategies.
* **ASCE Parser MCP Server:** Local tools for parsing `.axml`, fetching neighborhood context, inspecting immediate children, finding roots, managing shared system context, and writing targeted updates back to a case.
* **Schema-Aware Parsing:** The parser uses `schemas/ASCAD 2.0.xml` as the source of truth for node, link, and status-field metadata.

## System Map

```mermaid
flowchart TD
  U[User / OpenCode Chat] --> NS[Narrative Synthesizer]
  U --> AE[Assurance Evaluator]
  U --> TD[Top-Down Architect]
  U --> ADV[Adversarial Evaluator]

  NS -->|parse_assurance_case| MCP[MCP Server: asce_tools]
  AE -->|parse_assurance_case / get_assurance_neighborhood| MCP
  TD -->|get_root_claims / get_node_children| MCP
  ADV -->|get_assurance_neighborhood / write_defeater| MCP

  MCP --> G[(AXML Graph + Schema)]
  MCP --> C[(Shared System Context)]

  AE --> S1[Evidence Incorporation]
  AE --> S2[Calculation]
  AE --> S3[Decomposition]
  AE --> S4[Substitution]
  AE --> S5[Concretion]

  ADV --> R1[Rebutting Defeater]
  ADV --> R2[Undercutting Defeater]
  ADV --> R3[Undermining Defeater]

  TD --> S1
  TD --> S2
  TD --> S3
  TD --> S4
  TD --> S5
```

## Workflow Relationships

```mermaid
flowchart LR
  A[Parse AXML] --> B[Inspect Context]
  B --> C[Choose Workflow]
  C --> D1[Executive Briefing]
  C --> D2[Top-Down Traversal]
  C --> D3[Bottom-Up Claim Evaluation]
  C --> D4[Red-Team Defeater Scan]

  D1 --> E1[Summarize bottom line]
  D1 --> E2[Save system brief]
  D2 --> E3[Find roots]
  D2 --> E4[Walk children]
  D3 --> E5[Route to subagents]
  D4 --> E6[Generate defeaters]

  E2 --> F[(Shared Context)]
```

## Agent Relationships

```mermaid
graph TD
  AE[Assurance Evaluator] --> C[Concretion]
  AE --> EI[Evidence Incorporation]
  AE --> CAL[Calculation]
  AE --> DEC[Decomposition]
  AE --> SUB[Substitution]

  TD[Top-Down Architect] --> EI
  TD --> CAL
  TD --> DEC
  TD --> SUB
  TD --> C

  ADV[Adversarial Evaluator] --> RB[Rebutting Defeater]
  ADV --> UC[Undercutting Defeater]
  ADV --> UM[Undermining Defeater]

  NS[Narrative Synthesizer] --> MCP[MCP Server]
  MCP --> CTX[(System Context)]
```

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/AgenticAssuranceCases.git](https://github.com/yourusername/AgenticAssuranceCases.git)
   cd AgenticAssuranceCases
