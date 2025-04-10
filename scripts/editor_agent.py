# editor_agent.py
# Master script that runs the editorial agent end-to-end
# - Watches the input folder for new documents
# - Chunks them using editor_chunker
# - Sends each chunk to LLM via editor_reviewer
# - Compiles results into a final report using editor_report_writer
# - Logs all activity and moves processed files to an archive folder

import os
import time
from datetime import datetime
import shutil
import traceback
from editor_chunker import chunk_document
from editor_reviewer import review_chunks
from editor_report_writer import write_report

# --- Configuration ---
# --- Use absolute paths relative to the project root ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FOLDER = os.path.join(PROJECT_ROOT, "input_documents")
OUTPUT_FOLDER = os.path.join(PROJECT_ROOT, "output_reports")
PROCESSED_FOLDER = os.path.join(PROJECT_ROOT, "processed_documents")
LOG_FILE = os.path.join(PROJECT_ROOT, "logs/editor_logbook.csv")
SUPPORTED_EXTENSIONS = [".pdf", ".docx"]       # File types we can process
POLL_INTERVAL = 10                              # Time interval (in seconds) to poll for new files
TEST_MODE = False                               # If True, files won't be moved after processing

# --- Ensure directories exist ---
os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs("logs", exist_ok=True)

# --- Initialize log file if missing ---
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w') as log:
        log.write("filename,timestamp,total_score,verdict\n")

# --- Main file processing function ---
def process_file(filepath):
    filename = os.path.basename(filepath)
    print(f"\n🔍 Processing: {filename}")

    # 1. Chunk the document using editor_chunker
    chunks = chunk_document(filepath)

    # 2. Review all chunks using the LLM
    feedback_list, total_score, verdict = review_chunks(chunks)

    # 3. Write the compiled report to disk
    report_path = write_report(filename, feedback_list, total_score, verdict)

    # 4. Move the original file to the processed folder unless in test mode
    if not TEST_MODE:
        shutil.move(filepath, os.path.join(PROCESSED_FOLDER, filename))

    # 5. Log the completion with formatted timestamp
    with open(LOG_FILE, 'a') as log:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log.write(f"{filename},{timestamp},{total_score},{verdict}\n")

    print(f"✅ Completed: {filename}\n📄 Report saved to: {report_path}\n")

# --- Main loop to watch for new files ---
def main():
    print("📂 Editorial Agent is running. Watching for files...")

    # Process existing files on first run
    for fname in os.listdir(INPUT_FOLDER):
        fpath = os.path.join(INPUT_FOLDER, fname)
        if os.path.isfile(fpath) and fname.lower().endswith(tuple(SUPPORTED_EXTENSIONS)):
            try:
                process_file(fpath)
            except Exception as e:
                print(f"❌ Error processing {fname}: {e}")
                traceback.print_exc()

    # Now begin watching loop for new files
    processed_files = set(os.listdir(PROCESSED_FOLDER))

    try:
        while True:
            for fname in os.listdir(INPUT_FOLDER):
                fpath = os.path.join(INPUT_FOLDER, fname)

                # Debug log
                print(f"📁 Scanning: {fname}")

                # Check it's a new file with a supported extension
                if (os.path.isfile(fpath) and fname.lower().endswith(tuple(SUPPORTED_EXTENSIONS))
                        and fname not in processed_files):
                    try:
                        process_file(fpath)
                        processed_files.add(fname)
                    except Exception as e:
                        print(f"❌ Error processing {fname}: {e}")
                        traceback.print_exc()

            time.sleep(POLL_INTERVAL)  # Wait before scanning again

    except KeyboardInterrupt:
        print("\n👋 Gracefully shutting down the Editorial Agent.")

if __name__ == "__main__":
    main()
