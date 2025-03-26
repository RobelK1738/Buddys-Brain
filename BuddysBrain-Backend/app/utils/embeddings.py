from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text):
    if not text:
        return []  # or [0.0] * 768 as a fallback embedding
    return model.encode(text).tolist()
