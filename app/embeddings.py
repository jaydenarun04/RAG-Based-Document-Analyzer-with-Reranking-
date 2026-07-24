from sentence_transformers import SentenceTransformer

# Load the embedding model only once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(chunks):
    """
    Converts a list of text chunks into embeddings.
    """

    embeddings = embedding_model.encode(chunks)

    return embeddings