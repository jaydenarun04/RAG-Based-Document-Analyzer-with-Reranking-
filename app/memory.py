# =====================================================
# Conversation Memory
# =====================================================

MAX_HISTORY = 6
"""
6 messages =
3 User Questions
3 Assistant Answers
"""

conversation_history = []


def add_message(role: str, content: str):
    """
    Add a message to memory.

    If memory exceeds MAX_HISTORY,
    remove the oldest message.
    """

    conversation_history.append(
        {
            "role": role,
            "content": content
        }
    )

    if len(conversation_history) > MAX_HISTORY:
        conversation_history.pop(0)


def get_history():
    """
    Return recent conversation history.
    """

    return conversation_history


def clear_history():
    """
    Remove all conversation history.
    """

    conversation_history.clear()