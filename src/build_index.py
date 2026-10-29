
from pathlib import Path
import pickle
import re

import faiss
from sentence_transformers import SentenceTransformer

PROJECT_DIR = Path(__file__).resolve().parent.parent

CHUNKS_PATH = PROJECT_DIR / "data" / "documents" / "chunks_preview.txt"
INDEX_PATH = PROJECT_DIR / "data" / "faiss_index.bin"
METADATA_PATH = PROJECT_DIR / "data" / "chunks_metadata.pkl"

# Read the chunk preview
text = CHUNKS_PATH.read_text(encoding="utf-8")

# Extract each chunk's number, PDF page, and text
pattern = r"--chunk\s+(\d+)\s+\|\s+PDF page\s+(\d+)---\s*(.*?)(?=\n--chunk\s+\d+\s+\|\s+PDF page\s+\d+---|\Z)"

matches = re.findall(pattern, text, flags=re.DOTALL)

chunks = []

for chunk_number, page_number, chunk_text in matches:
    chunk_text = chunk_text.strip()

    if chunk_text:
        chunks.append({
            "chunk_id": int(chunk_number),
            "page": int(page_number),
            "text": chunk_text
        })

if not chunks:
    raise ValueError(
        "No chunks were parsed. Check the format of chunks_preview.txt."
    )

print("Total chunks loaded:", len(chunks))

# Create embeddings from the chunk text
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

texts = [chunk["text"] for chunk in chunks]

vectors = model.encode(
    texts,
    convert_to_numpy=True,
    show_progress_bar=True,
    normalize_embeddings=True,
)

print("Vector shape:", vectors.shape)

# Build the FAISS similarity-search index
dimension = vectors.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(vectors)

# Save the index and structured chunk metadata
faiss.write_index(index, str(INDEX_PATH))

with METADATA_PATH.open("wb") as file:
    pickle.dump(chunks, file)

print("FAISS index saved to:", INDEX_PATH)
print("Chunk metadata saved to:", METADATA_PATH)
print("Total vectors indexed:", index.ntotal)
print("First chunk PDF page:", chunks[0]["page"])
