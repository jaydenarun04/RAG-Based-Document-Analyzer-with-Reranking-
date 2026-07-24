import chromadb
from app.embeddings import embedding_model

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="pdf_chunks"
)


def retrieve_chunks(question, top_k=5):

    question_embedding = embedding_model.encode(question)

    results = collection.query(
        query_embeddings=[question_embedding.tolist()],
        n_results=top_k
    )

    return results