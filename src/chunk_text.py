
from pathlib import Path
import re

PROJECT_DIR = Path(__file__).resolve().parent.parent

TEXT_PATH = (
    PROJECT_DIR
    / "data"
    / "documents"
    / "infosys_annual_report.txt"
)

OUTPUT_PATH = (
    PROJECT_DIR
    / "data"
    / "documents"
    / "chunks_preview.txt"
)

full_text = TEXT_PATH.read_text(encoding="utf-8")

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

chunks = []

# Split the report using its page markers
pages = re.split(r"---page(\d+)----", full_text)

# The split produces alternating text sections and page numbers.
for i in range(1, len(pages), 2):
    page_number = int(pages[i])
    page_text = pages[i + 1].strip()

    if not page_text:
        continue

    start = 0

    while start < len(page_text):
        end = min(start + CHUNK_SIZE, len(page_text))
        chunk_text = page_text[start:end].strip()

        if chunk_text:
            chunks.append({
                "page": page_number,
                "text": chunk_text
            })

        if end == len(page_text):
            break

        start = end - CHUNK_OVERLAP

print("Total pages with text:", len(set(c["page"] for c in chunks)))
print("Total chunks:", len(chunks))

print("\n========== FIRST CHUNK ==========")
print("PDF page:", chunks[0]["page"])
print(chunks[0]["text"])

with OUTPUT_PATH.open("w", encoding="utf-8") as file:
    for chunk_number, chunk in enumerate(chunks, start=1):
        file.write(f"\n--chunk {chunk_number} | PDF page {chunk['page']}---\n")
        file.write(chunk["text"])
        file.write("\n")

print("\nChunk preview saved to:", OUTPUT_PATH)
