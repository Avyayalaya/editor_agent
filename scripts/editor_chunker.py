# editor_chunker.py
# Extracts and chunks documents into page-based sections for editorial review
# Returns both the chunk text and its page range for reference

import pdfplumber
from docx import Document as DocxDocument
import os

# --- Determine chunk size dynamically based on total pages ---
def determine_chunk_size(page_count):
    if page_count <= 20:
        return 2
    elif page_count <= 100:
        return 5
    elif page_count <= 200:
        return 10
    else:
        return 15

# --- PDF Processing ---
def extract_pdf_text(filepath):
    pages = []
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text.strip())
    return pages

# --- DOCX Processing ---
def extract_docx_text(filepath):
    doc = DocxDocument(filepath)
    paragraphs = [para.text.strip() for para in doc.paragraphs if para.text.strip() != ""]
    page_estimate = max(1, len(paragraphs) // 40)
    chunk_size = determine_chunk_size(page_estimate)

    chunks = []
    for i in range(0, len(paragraphs), 40 * chunk_size):
        start_page = (i // 40) + 1
        end_page = ((i + 40 * chunk_size - 1) // 40) + 1
        text = "\n\n".join(paragraphs[i:i + 40 * chunk_size])
        chunks.append({"chunk_text": text, "start_page": start_page, "end_page": end_page})

    return chunks

# --- Chunk a document regardless of type ---
def chunk_document(filepath):
    _, ext = os.path.splitext(filepath)
    ext = ext.lower()

    if ext == ".pdf":
        pages = extract_pdf_text(filepath)
        chunk_size = determine_chunk_size(len(pages))

        chunks = []
        for i in range(0, len(pages), chunk_size):
            start_page = i + 1
            end_page = min(i + chunk_size, len(pages))
            text = "\n\n".join(pages[i:i + chunk_size])
            chunks.append({"chunk_text": text, "start_page": start_page, "end_page": end_page})

    elif ext == ".docx":
        chunks = extract_docx_text(filepath)

    else:
        raise ValueError("Unsupported file type for chunking.")

    return chunks
