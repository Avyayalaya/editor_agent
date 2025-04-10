# editor_reviewer.py
# Sends each chunk to the LLM using the expert editorial prompt and aggregates results

import openai
import os
from dotenv import load_dotenv  # Load environment variables from .env file

# --- Load .env file ---
load_dotenv()  # Looks for a file named '.env' in the project root by default

# --- Set your API key from environment variable ---
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Custom editorial prompt v1.1 ---
EDITORIAL_PROMPT = """
You are a professional book editor with deep expertise in grammar, clarity, structure, and formatting. 
Your job is to critically review a section from a manuscript (5–20 pages) and return a highly structured, 
honest, and actionable editorial report.

Focus on the following two main sections:

### 1. LANGUAGE & MECHANICS (Priority Focus)
Evaluate for:
- Grammar, spelling, punctuation
- Sentence construction and flow
- Redundancies and awkward phrasing
- OCR or formatting artifacts (e.g., repeated words, inconsistent spacing)

### 2. STRUCTURE, CLARITY & ENGAGEMENT
Evaluate for:
- Logical structure and flow
- Tone and voice consistency
- Accuracy of explanations
- Educational or narrative effectiveness
- Visual layout, formatting, and user experience

For each section:
1. Assign a score from 1 (poor) to 5 (excellent)
2. List key issues with examples
3. Suggest specific improvements or rewrites

### SUMMARY:
- Table of scores
- Total score (out of 10)
- Verdict (choose one): ✅ Publication-ready / ✏️ Needs minor revision / 🛠 Substantial editing needed / 🔄 Rewrite recommended
- 3–5 bullet-point priority improvements

Do not rewrite the original. Focus on review, analysis, and guidance.
"""

# --- Send chunk to GPT and get structured feedback ---
def review_chunk(chunk):
    try:
        print("🚀 Sending chunk to OpenAI...")

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert editorial assistant."},
                {"role": "user", "content": f"{EDITORIAL_PROMPT}\n\nHere is the section to review:\n---\n{chunk}\n---"}
            ],
            temperature=0.4,
            max_tokens=1500
        )

        print("✅ Response received from OpenAI.")
        return response["choices"][0]["message"]["content"]

    except Exception as e:
        print(f"❌ API call failed: {e}")
        import traceback
        traceback.print_exc()
        return f"Error: {e}"

# --- Review all chunks and summarize total score and verdict ---
def review_chunks(chunks):
    feedback_list = []
    total_score = 0
    verdict = ""

    for i, chunk_info in enumerate(chunks):
        print(f"🧠 Reviewing chunk {i+1}/{len(chunks)}...")
        chunk_text = chunk_info["chunk_text"]
        feedback = review_chunk(chunk_text)

        # ✅ Append full chunk metadata, not just a label string
        feedback_list.append((chunk_info, feedback))

        # Optional: parse numeric score and verdict from response
        if "Total score" in feedback:
            try:
                score_line = [line for line in feedback.splitlines() if "Total score" in line][0]
                score = int("".join(filter(str.isdigit, score_line)))
                total_score += score
            except:
                pass

        if not verdict:
            for v in ["Publication-ready", "Needs minor revision", "Substantial editing needed", "Rewrite recommended"]:
                if v in feedback:
                    verdict = v

    average_score = total_score // len(chunks) if chunks else 0
    return feedback_list, average_score, verdict
