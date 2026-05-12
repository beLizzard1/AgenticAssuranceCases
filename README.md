# Agentic Assurance Cases

This repository contains an OpenCode-based environment for evaluating Claim-Argument-Evidence (CAE) assurance cases using the Helping Hand notation. It uses a local Model Context Protocol (MCP) server to parse and inspect Adelard ASCE `.axml` files as structured graphs instead of raw XML.

## Features
* **Assurance Evaluator Agent:** The primary agent that routes claims to the right justification strategy.
* **Top-Down Architect Agent:** A root-first orchestrator that walks the assurance tree downward using targeted MCP navigation tools.
* **Specialized Assurance Subagents:** Evidence Incorporation, Calculation, Decomposition, Substitution, and Concretion.
* **Adversarial Evaluator Agent:** A red-team pass with rebutting, undercutting, and undermining defeater strategies.
* **ASCE Parser MCP Server:** Local tools for parsing `.axml`, fetching neighborhood context, inspecting immediate children, finding roots, and writing targeted updates back to a case.
* **Schema-Aware Parsing:** The parser uses `schemas/ASCAD 2.0.xml` as the source of truth for node, link, and status-field metadata.

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/AgenticAssuranceCases.git](https://github.com/yourusername/AgenticAssuranceCases.git)
   cd AgenticAssuranceCases
