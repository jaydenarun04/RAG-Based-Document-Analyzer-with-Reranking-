# =====================================================
# Prompt Builder
# =====================================================

def build_prompt(question: str, chunks: list, history: list):

    # Join retrieved chunks
    context = "\n\n".join(chunks)

    # Build conversation history
    if history:

        conversation = "\n".join(
            f"{message['role'].capitalize()}: {message['content']}"
            for message in history
        )

    else:

        conversation = "No previous conversation."

    prompt = f"""
You are an intelligent AI assistant that answers questions ONLY from the provided PDF context.

Rules:
1. Answer ONLY from the provided context.
2. Do NOT make up information.
3. If the answer is not present in the context, reply exactly:
   "I couldn't find that information in the uploaded PDF."
4. Keep the answer concise and clear.
5. If the user asks a follow-up question, use the conversation history to understand the context.

======================================================
Conversation History
======================================================

{conversation}

======================================================
Retrieved Context
======================================================

{context}

======================================================
Current Question
======================================================

{question}

======================================================
Answer
======================================================
"""

    return prompt