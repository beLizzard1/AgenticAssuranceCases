# Agentic Assurance Cases

This repository contains an AI-driven environment for evaluating Claim-Argument-Evidence (CAE) assurance cases using the Helping Hand notation. It is built natively for [OpenCode](https://opencode.ai/) and utilizes the Model Context Protocol (MCP).

## Features
* **Assurance Evaluator Agent:** A primary OpenCode agent that routes claims to specific justification strategies.
* **Specialized Subagents:** Handlers for Evidence Incorporation, Calculation, Decomposition, Substitution, and Concretion.
* **ASCE Parser MCP Server:** A custom tool that allows the agents to ingest and map `.axml` network files efficiently.

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/AgenticAssuranceCases.git](https://github.com/yourusername/AgenticAssuranceCases.git)
   cd AgenticAssuranceCases
