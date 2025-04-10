# 🛠️ Agent Building Guide — Editorial Agent Pattern

This guide captures the reusable design pattern for building local-first, document-aware, GPT-powered agents. Based on the Editorial Agent implementation, this is a blueprint you can adapt to any problem where structured review, analysis, or transformation is needed across files.

---

## 1. 🧭 Core Philosophy
An agent is not just a single script or a single LLM call. It is a structured, autonomous system composed of modular components that work together, triggered by input events, guided by a clear persona, and validated at every stage.

---

## 2. 🧩 Agent Components

| Component         | Responsibility                                              |
|------------------|--------------------------------------------------------------|
| Watcher          | Monitors input folder and triggers workflow per new file     |
| Chunker          | Splits input document into reviewable sections (pages/logic) |
| Reviewer         | Sends each chunk to LLM with domain-specific prompt          |
| Validator        | Ensures LLM output meets required structure                  |
| Report Writer    | Aggregates and formats output into human-usable doc          |
| Logger           | Tracks actions and verdicts in a structured history file     |

---

## 3. 🧱 Agent Script Layout
```
/editorial-agent/
├── scripts/
│   ├── editor_agent.py
│   ├── editor_chunker.py
│   ├── editor_reviewer.py
│   ├── editor_report_writer.py
│   └── utils.py (optional)
├── input_documents/
├── output_reports/
├── logs/
├── .env
├── README.md
```

---

## 4. 🧠 Building the Agent Step-by-Step

### Step 1: Define the Use Case
```md
- What does the agent act on? (files, folders, queries)
- What is the expected output?
- Who is the user? What pain point does this solve?
```

### Step 2: Define the Agent's Architecture
- Diagram the agent lifecycle from input to output
- Decide on file flow and state tracking (folder structure, logs)

### Step 3: Implement Scripts Modularly
Each script should be:
- Independently testable
- Clear about its inputs/outputs
- Responsible only for its role

### Step 4: Craft the LLM Prompt
- Create a structured prompt with:
  - Scoring framework
  - Sectional expectations
  - Summary and recommendations
- Use variable placeholders for chaining (e.g. `{{chunk_text}}`, `{{score}}`)

### Step 5: Embed Validation Logic
- Use assert statements or conditionals to check:
  - Prompt sections exist
  - Scores/verdicts are valid
  - API key is loaded

### Step 6: Run the Agent Locally
- Start the file watcher script
- Drop test files in the input folder
- Review log output and generated report

### Step 7: Debug & Extend
- Add print/debug messages at each stage
- Create error handling: if file is open, if chunking fails, if API errors out

---

## 5. ✅ Embedded Tests & Checkpoints
Every script should have at least one test:

### In `editor_chunker.py`
```python
assert len(chunks) > 0
assert "chunk_text" in chunks[0]
```

### In `editor_reviewer.py`
```python
assert "Total Score" in feedback
assert any(v in feedback for v in ["✅", "✏️", "🛠", "🔄"])
```

### In `editor_report_writer.py`
```python
assert os.path.exists(report_path)
```

---

## 6. 🧠 Editorial Persona Behavior
Your LLM prompt should encode these behaviors:
- Be honest but constructive
- Do not rewrite, only suggest
- Score consistently
- Provide a final verdict
- Always return all sections (no hallucinated omissions)

---

## 7. 🔗 Chaining & Variable Management
Variables passed across agents:
```md
- filename → used in all logs and reports
- chunk → contains chunk_text + page_start + page_end
- feedback → passed to report generator
- verdict → logged to logbook
```
Use dictionaries and structured tuples for clarity.

---

## 8. 📦 Packaging for GitHub
Include:
- `.env.example`
- `requirements.txt`
- `README.md` and `product_brief.md`
- Sample input and output files
- Clear instructions in top-level `README`

---

## 9. 🧬 Replicating the Pattern
To adapt this agent pattern to other domains:
- Change the prompt logic in reviewer
- Adjust chunking strategy (semantic instead of pages)
- Replace output doc with a different format (PDF, JSON)
- Add frontend or API layer on top of watcher

---

## 10. 🔮 Next-Level Ideas
- Multi-agent orchestration
- Plugin support (spellcheck, bias flags, custom templates)
- Scheduled cron-based review instead of file watching
- Web UI for triggering runs and visualizing outputs

---

This guide + the scaffold prompt + the working repo = your full blueprint for building autonomous LLM agents with real-world utility.

Iterate fast. Test often. Ship meaningfully.

