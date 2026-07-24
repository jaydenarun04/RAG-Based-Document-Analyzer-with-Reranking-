import requests
import streamlit as st

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="Advanced PDF RAG Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Advanced PDF RAG Analyzer")
st.write("Upload one or more PDFs and ask questions about them.")

BASE_URL = "http://127.0.0.1:8000"

# =====================================================
# Session State
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================================================
# Sidebar
# =====================================================

with st.sidebar:

    st.header("Options")

    if st.button("🗑️ Clear Conversation"):

        requests.post(f"{BASE_URL}/clear-memory")

        st.session_state.messages = []

        st.success("Conversation Cleared!")

        st.rerun()

# =====================================================
# Upload Multiple PDFs
# =====================================================

uploaded_files = st.file_uploader(
    "Choose PDF(s)",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    if st.button("📤 Upload PDF(s)"):

        progress_bar = st.progress(0)

        total_files = len(uploaded_files)

        success_count = 0

        for index, uploaded_file in enumerate(uploaded_files):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    "application/pdf"
                )
            }

            response = requests.post(
                f"{BASE_URL}/upload",
                files=files
            )

            if response.status_code == 200:
                success_count += 1

            progress_bar.progress((index + 1) / total_files)

        st.success(
            f"✅ Uploaded {success_count} of {total_files} PDF(s) successfully!"
        )

# =====================================================
# Display Chat History
# =====================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =====================================================
# Chat Input
# =====================================================

question = st.chat_input(
    "Ask a question about the uploaded PDFs..."
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = requests.get(
                f"{BASE_URL}/search",
                params={
                    "question": question
                }
            )

            if response.status_code == 200:

                answer = response.json()["answer"]

            else:

                answer = "Something went wrong."

        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )