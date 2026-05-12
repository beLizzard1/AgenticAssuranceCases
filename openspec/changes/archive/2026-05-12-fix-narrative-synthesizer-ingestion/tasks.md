## 1. Narrative Synthesizer Prompt

- [x] 1.1 Update `.opencode/agents/narrative-synthesizer.md` so both modes explicitly use `parse_assurance_case` as the ingest path.
- [x] 1.2 Remove or replace any prompt language that implies direct `.axml` text reading or file scraping.
- [x] 1.3 Confirm the prompt still routes the context-generation mode through `set_system_context`.

## 2. Validation

- [x] 2.1 Validate the executive briefing mode against the sample `.axml` file and confirm the output is based on parsed graph data.
- [x] 2.2 Validate the context-generation mode against the sample `.axml` file and confirm the saved shared brief is reusable by downstream agents.
