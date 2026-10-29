from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# load the embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# examples creating
passages=[
    "Infosys reported its annual revenue and financial performance.",
    "The company discusses risks related to cybersecurity.",
    "The report describes employee training and development programs.",
]

# write a question
question = "what risks does infosys face from cyber attack"

# CONVERT passages and questions into vectors
passages_vectors = model.encode(passages)
question_vector = model.encode([question])

#scores
scores = cosine_similarity(question_vector, passages_vectors)[0]
# calculate similarity scores
best_index =scores.argmax()


print("Question:", question)
print("\nMost relevant passage:")
print(passages[best_index])
print("\nSimilarity score:", round(float(scores[best_index]), 4))