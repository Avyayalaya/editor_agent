# 📚 Editorial Agent

The Editorial Agent is a local-first AI assistant that watches a folder, reads incoming `.pdf` and `.docx` documents, intelligently chunks them, reviews each part using GPT-4o, and generates a detailed editorial feedback report — all fully automated.

## ✨ Why Use This?
- Designed for teachers, authors, curriculum designers, and editors
- Helps polish drafts, books, lesson plans, or study material
- Offers structured, human-grade editorial feedback
- No manual uploading — just drop a file and let the agent do the work

## 🛠 How It Works
```
input_documents/  →  🔍 chunked and reviewed →  output_reports/
                                   ↓
                         logs/editor_logbook.csv
```

### Main Components:
- `editor_agent.py` – Orchestrates the full flow
- `editor_chunker.py` – Breaks long documents into smart chunks
- `editor_reviewer.py` – Sends each chunk to OpenAI with a powerful editorial prompt
- `editor_report_writer.py` – Compiles a polished Word doc with feedback

## 📦 Getting Started
### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/editorial-agent.git
cd editorial-agent
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Add Your API Key
Create a `.env` file:
```bash
OPENAI_API_KEY=sk-...your-key-here...
```

### 4. Run the Agent
```bash
python scripts/editor_agent.py
```

Drop files into `input_documents/` and watch them get processed. Reports are saved to `output_reports/`.

## 📄 Sample Output
See `sample_output/report_example.docx`

## 🔍 Example Use Cases
- Reviewing K-12 textbooks
- Improving instructional design for teachers
- Editing fiction or non-fiction drafts
- Flagging clarity or grammar issues in training content

## 💡 Roadmap Ideas
- Export to PDF
- Live web interface
- Team dashboard for tracked feedback
- Built-in style guides

## 📜 License
MIT — use it, build on it, share it.

## 🧠 Inspired by a Live Agent Build
This project was built step-by-step using AI. See `agent_building_guide.md` for how to create your own AI agent from scratch.

---
Let the agent edit while you create.

