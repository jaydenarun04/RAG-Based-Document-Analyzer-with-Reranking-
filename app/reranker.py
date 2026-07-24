from sentence_transformers import CrossEncoder

# Load the reranker model
reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank(question, retrieved_chunks, top_n=3):
    """
    Re-rank retrieved chunks using a Cross Encoder.
    """

    # Create (question, chunk) pairs
    pairs = []

    for chunk in retrieved_chunks:
        pairs.append((question, chunk))

    # Predict relevance scores
    scores = reranker.predict(pairs)

    # Combine chunks with scores
    ranked = list(zip(retrieved_chunks, scores))

    # Sort by score (highest first)
    ranked.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return ranked[:top_n]