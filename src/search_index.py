
from pathlib import Path
import pickle

import faiss
from sentence_transformers import SentenceTransformer

PROJECT_DIR = Path(__file__).resolve().parent.parent

INDEX_PATH = PROJECT_DIR / "data" / "faiss_index.bin"
METADATA_PATH = PROJECT_DIR / "data" / "chunks_metadata.pkl"

# Load the FAISS index
index = faiss.read_index(str(INDEX_PATH))

# Load chunk text and page metadata
with METADATA_PATH.open("rb") as file:
    chunks = pickle.load(file)

# Load the embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Ask a question
question = "What were Infosys's revenue and net profit for fiscal year 2026?"

# Convert the question into an embedding
question_vector = model.encode(
    [question],
    convert_to_numpy=True,
    normalize_embeddings=True,
)

# Retrieve the three most relevant chunks
scores, indices = index.search(question_vector, 3)

print("\nQuestion:", question)

for rank, (score, chunk_index) in enumerate(
    zip(scores[0], indices[0]), start=1
):
    if chunk_index < 0:
        continue

    chunk = chunks[int(chunk_index)]

    print(f"\n{'=' * 20} Result {rank} {'=' * 20}")
    print("Similarity score:", round(float(score), 4))
    print("Chunk number:", chunk["chunk_id"])
    print("PDF page:", chunk["page"])
    print("\nRetrieved text:\n")
    print(chunk["text"])
