
from pathlib import Path
import os
import pickle

import faiss
from groq import Groq
from sentence_transformers import SentenceTransformer

# 1. Find the project files
PROJECT_DIR = Path(__file__).resolve().parent.parent
INDEX_PATH = PROJECT_DIR / "data" / "faiss_index.bin"
METADATA_PATH = PROJECT_DIR / "data" / "chunks_metadata.pkl"

# 2. Load the FAISS index and chunk metadata
index = faiss.read_index(str(INDEX_PATH))

with METADATA_PATH.open("rb") as file:
    chunks = pickle.load(file)

# 3. Load the embedding model
embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# 4. Connect to Groq
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY is not set. Set it in your PowerShell terminal first."
    )

client = Groq(api_key=api_key)

# 5. Ask a question
question = input("Ask a question about the Infosys annual report: ")

# 6. Retrieve the five most relevant chunks
question_vector = embedding_model.encode(
    [question],
    convert_to_numpy=True,
    normalize_embeddings=True,
)

scores, indices = index.search(question_vector, 8)

retrieved_chunks = []

for rank, chunk_index in enumerate(indices[0], start=1):
    if chunk_index == -1:
        continue

    chunk = chunks[int(chunk_index)]

    retrieved_chunks.append(
        f"[PDF page {chunk['page']}]\n{chunk['text']}"
    )

context = "\n\n".join(retrieved_chunks)

# Display the retrieved sources for debugging
print("\n" + "=" * 50)
print("RETRIEVED SOURCE PASSAGES")
print("=" * 50)
print(context)

# 7. Generate a grounded answer using Groq
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "system",
            "content": (
                "You are DocuRAG, a document question-answering assistant. "
                "Use only information explicitly stated in the supplied passages. "
                "Do not introduce facts from outside the passages. "
                "Preserve financial metric names, values, units, and reporting periods. "
                "Cite each factual claim using the exact source label provided, "
                "such as [PDF page 163]. "
                "Place citations immediately after the claims they support. "
                "Never invent page numbers or cite a page that does not support the claim. "
                "Separate actual risks or threats from controls, monitoring activities, "
                "and governance arrangements; label each category accurately. "
                "Never present a control or governance arrangement as proof of a weakness "
                "or gap unless the supplied passages explicitly confirm that weakness. "               
                "Do not describe a weakness, failure, or gap unless the passages "
                "explicitly establish that it exists. "
                "If a requested fact is missing, say so. "
                "Avoid unsupported conclusions and business opinions. "
                "Be concise and follow any requested word limit."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Question: {question}\n\n"
                f"Report passages:\n{context}"
            ),
        },
    ],
    temperature=0.1,
    max_completion_tokens=2048,
    include_reasoning=False,
    reasoning_effort="low",
)

print("\n" + "=" * 50)
print("DOCURAG ANSWER")
print("=" * 50)
print(response.choices[0].message.content)
