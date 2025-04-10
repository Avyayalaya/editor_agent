# 🧠 Editorial Agent: Master Prompt Scaffold (v1.0)

This Markdown document serves as a complete, chainable master prompt and build template for constructing an intelligent, file-watching, LLM-powered editorial review agent. It includes scoped variables, embedded validation checkpoints, structured personas, script orchestration logic, and markdown-defined test cases.

Use this to:
- Reproduce the architecture for similar agents
- Build structured agent pipelines with feedback loops
- Deploy document-based LLM systems that are verifiable, testable, and extensible

---

## 1. 🎯 PROBLEM DEFINITION
```
GOAL: Automatically review documents (PDF or DOCX) dropped into a folder
OUTPUT: Human-grade, structured editorial feedback report
USERS: Teachers, editors, authors, education designers
PAIN_POINTS:
  - Reviewing long files manually is slow
  - Generic AI tools give inconsistent feedback
  - Lack of structure in AI outputs makes them hard to act on
```

---

## 2. 🏗 AGENT ARCHITECTURE OVERVIEW
```
AGENT_NAME: EditorialAgent
WORKFLOW:
  1. Watch input folder for new files
  2. Chunk file into page-based or semantic units
  3. Pass each chunk to GPT using a structured editorial prompt
  4. Parse and validate feedback
  5. Aggregate and generate a formatted Word (.docx) report
  6. Move file to archive and log review result
```

```mermaid
graph TD
    Watcher --> Chunker --> Reviewer --> Validator --> Reporter --> Logger
```

---

## 3. 🧩 SCRIPT DEFINITIONS

### 3.1 `editor_agent.py`
```
ROLE: Orchestrator
INPUTS: Directory path, API key
OUTPUTS: Initiates full pipeline per file
CHECKPOINTS:
  - File extension validation
  - Log creation and report path confirmation
```

### 3.2 `editor_chunker.py`
```
ROLE: Chunk documents by page or semantic header
INPUTS: Filepath (PDF or DOCX)
OUTPUTS: List of {chunk_text, start_page, end_page}
VARIABLES:
  - CHUNK_SIZE based on document length
TEST CASES:
  - 5-page doc = 1 chunk
  - 60-page doc = ~6 chunks
```

### 3.3 `editor_reviewer.py`
```
ROLE: Feed chunk to GPT and return structured review
INPUTS: chunk_text
OUTPUTS: feedback block with scores + verdict
VALIDATION:
  - Are sections "Language", "Structure", and "Summary" present?
  - Is total score parsable?
```

### 3.4 `editor_report_writer.py`
```
ROLE: Save all chunk feedback as a formatted .docx file
INPUTS: feedback_list, original_filename
OUTPUTS: Saved Word document in output_reports/
STYLE:
  - Heading per chunk with page range
  - Horizontal lines between chunks
  - Summary section at top
TEST:
  - Does the file overwrite if it already exists?
  - Can all sections be read in Word?
```

### 3.5 `.env`
```
Stores: OPENAI_API_KEY
CHECK: Must be loaded in `editor_reviewer.py`
```

---

## 4. 🧠 EDITORIAL REVIEWER PROMPT
```markdown
SYSTEM:
You are an expert editorial assistant.

USER:
Review the following section from a manuscript. Your job is to give a detailed editorial evaluation using the format below:

### Language & Mechanics (Score: 1–5)
- [issues]

### Structure & Clarity (Score: 1–5)
- [issues]

### Summary
- Total Score: x / 10
- Verdict: [choose one: ✅ / ✏️ / 🛠 / 🔄]
- Top 3–5 improvement suggestions
```

---

## 5. 🔗 CHAINED VARIABLES FLOW
```
chunk_document(filepath) → [chunk_text, page_start, page_end]
→ review_chunk(chunk_text) → structured_feedback
→ write_report(feedback_list) → docx_path
→ log_verdict(filename, score, verdict)
```

---

## 6. ✅ EMBEDDED TEST & CHECKPOINTS
```python
# In editor_agent.py
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w') as f: f.write("filename,timestamp,score,verdict\n")

# In reviewer
assert 'Total Score' in feedback
assert any(v in feedback for v in ["Publication-ready", "Needs minor revision"])

# In writer
assert os.path.exists(report_path), "File did not save."
```

---

## 7. 📄 OUTPUT STYLING FORMAT (for report_writer)
```
📛 Title: Editorial Feedback Report
🧾 Metadata: Filename, Date, Verdict, Score
📚 Sections:
  - Chunk Heading (with Page Range)
  - Language & Mechanics
  - Structure & Clarity
  - Summary + Recommendations
📏 Styling:
  - Font: 11pt, Serif or Default
  - Chunk separator: ———
  - Page-aligned bullets
```

---

## 8. 🔁 REUSE BLOCK: BUILDING NEW AGENTS
```
To build a new agent (e.g., policy reviewer, academic summarizer):
1. Replace `editorial_prompt.md` with your domain-specific criteria
2. Update `chunker.py` logic to extract per-section or semantic blocks
3. Modify scoring logic in `reviewer.py`
4. Adjust output format and naming
5. Re-test using dummy files in `input_documents/`
```

---

## 9. 📚 GLOSSARY
```
CHUNK_SIZE: Number of pages or semantic blocks per review unit
VERDICT: Editorial recommendation (✅/✏️/🛠/🔄)
FEEDBACK_LIST: List of (chunk_metadata, feedback) tuples
DOCX_PATH: Final report location
```

---

## 10. 🔒 FAIL-SAFE HOOKS
```
If OpenAI API key is not found:
  raise ValueError("API key missing")

If chunk fails to generate:
  skip and log as "Chunk parse error"

If review fails structure check:
  re-prompt with "Please include all required sections."

If docx fails to save:
  warn and write fallback .txt
```

---

Use this document as your reproducible, modular, testable blueprint to build and extend editorial agents — or any document-first LLM pipeline.
