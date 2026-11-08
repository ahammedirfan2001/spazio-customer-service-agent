
import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# Project directories
BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_DIR = BASE_DIR / "data" / "knowledge_base"
VECTOR_DIR = BASE_DIR / "vector_store"

INDEX_PATH = VECTOR_DIR / "knowledge.index"
METADATA_PATH = VECTOR_DIR / "metadata.json"

# Embedding model
MODEL_NAME = "all-MiniLM-L6-v2"

# Load the embedding model once when the application starts
model = SentenceTransformer(MODEL_NAME)

# Load the FAISS index once when the application starts
index = faiss.read_index(str(INDEX_PATH)) if INDEX_PATH.exists() else None

def load_documents():
    """Load all Markdown documents from the knowledge-base folder."""

    documents = []

    for file_path in KNOWLEDGE_DIR.glob("*.md"):
        content = file_path.read_text(encoding="utf-8")

        if content.strip():
            documents.append({
                "source": file_path.name,
                "content": content
            })

    return documents


def split_into_chunks(text, chunk_size=700, overlap=100):
    """Split document text into overlapping chunks."""

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def build_knowledge_base():
    """Create embeddings and save the FAISS index."""

    print("Using the loaded embedding model...")

    print("Reading restaurant documents...")
    documents = load_documents()

    if not documents:
        print("No Markdown documents found!")
        return

    all_chunks = []
    metadata = []

    for document in documents:
        chunks = split_into_chunks(document["content"])

        for chunk in chunks:
            all_chunks.append(chunk)
            metadata.append({
                "source": document["source"],
                "content": chunk
            })

    print(f"Created {len(all_chunks)} text chunks.")

    print("Generating embeddings...")
    embeddings = model.encode(
        all_chunks,
        normalize_embeddings=True,
        convert_to_numpy=True
    )

    embeddings = np.asarray(embeddings, dtype="float32")

    print("Building FAISS index...")
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    VECTOR_DIR.mkdir(parents=True, exist_ok=True)

    faiss.write_index(index, str(INDEX_PATH))

    with open(METADATA_PATH, "w", encoding="utf-8") as file:
        json.dump(metadata, file, ensure_ascii=False, indent=4)

    print("\nKnowledge base created successfully!")
    print(f"Documents: {len(documents)}")
    print(f"Chunks: {len(all_chunks)}")



def search_knowledge(query, top_k=3):
    """Find the most relevant knowledge-base chunks."""

    if not INDEX_PATH.exists() or not METADATA_PATH.exists():
        return "Knowledge base not found. Please build it first."

    if index is None:
        return "Knowledge base index is not loaded. Please rebuild it."



    with open(METADATA_PATH, "r", encoding="utf-8") as file:
        metadata = json.load(file)

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True,
        convert_to_numpy=True
    )

    query_embedding = np.asarray(query_embedding, dtype="float32")

    scores, indices = index.search(query_embedding, top_k)

    results = []

    # Minimum similarity score for accepting a result

    MIN_SCORE = 0.35

    for score, idx in zip(scores[0], indices[0]):

        if idx == -1 or score < MIN_SCORE:
            continue

        results.append({
            "source": metadata[idx]["source"],
            "content": metadata[idx]["content"],
            "score": float(score)
        })

    return results


if __name__ == "__main__":
    build_knowledge_base()
