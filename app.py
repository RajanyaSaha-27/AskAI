import os
import tempfile

import streamlit as st

from AskAI.document_loaders.pdf_loader import load_pdf
from AskAI.create_chroma import create_vector_database
from AskAI.main import create_llm, ask_question


# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="PDF RAG Assistant",
    page_icon="📚",
    layout="centered"
)


# ==========================================
# Title
# ==========================================

st.title("📚 PDF RAG Assistant")

st.write(
    "Upload a PDF and ask questions based on its content."
)


# ==========================================
# Session State
# ==========================================

if "vector_db" not in st.session_state:
    st.session_state.vector_db = None

if "llm" not in st.session_state:
    st.session_state.llm = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None


# ==========================================
# Initialize LLM
# ==========================================

if st.session_state.llm is None:

    try:

        st.session_state.llm = create_llm()

    except Exception as error:

        st.error("Could not initialize Gemini.")

        st.code(str(error))

        st.stop()


# ==========================================
# PDF Upload
# ==========================================

st.subheader("📄 Upload PDF")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)


# ==========================================
# Process PDF
# ==========================================

if uploaded_file is not None:

    st.info(
        f"Selected PDF: **{uploaded_file.name}**"
    )


    if st.button(
        "🚀 Process PDF",
        use_container_width=True
    ):

        with st.spinner(
            "Loading and processing PDF..."
        ):

            try:

                # -----------------------------
                # Save uploaded PDF temporarily
                # -----------------------------

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as temp_file:

                    temp_file.write(
                        uploaded_file.getvalue()
                    )

                    temp_pdf_path = temp_file.name


                # -----------------------------
                # Load PDF
                # -----------------------------

                documents = load_pdf(
                    temp_pdf_path
                )


                # -----------------------------
                # Create Chroma database
                # -----------------------------

                vector_db = create_vector_database(
                    documents
                )


                # -----------------------------
                # Store in session
                # -----------------------------

                st.session_state.vector_db = vector_db

                st.session_state.pdf_name = (
                    uploaded_file.name
                )


                # Reset previous conversation

                st.session_state.messages = []


                # Delete temporary file

                os.remove(temp_pdf_path)


                st.success(
                    "✅ PDF processed successfully!"
                )


            except Exception as error:

                st.error(
                    "Failed to process the PDF."
                )

                st.code(str(error))


# ==========================================
# Processing Status
# ==========================================

if st.session_state.vector_db is not None:

    st.success(
        f"📖 Ready to answer questions from: "
        f"**{st.session_state.pdf_name}**"
    )


# ==========================================
# Chat History
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        if (
            message["role"] == "assistant"
            and message.get("sources")
        ):

            st.caption(
                "Sources: "
                + ", ".join(
                    message["sources"]
                )
            )


# ==========================================
# Chat Input
# ==========================================

question = st.chat_input(
    "Ask something about the PDF..."
)


if question:

    # -----------------------------
    # Check PDF
    # -----------------------------

    if st.session_state.vector_db is None:

        st.warning(
            "Please upload and process a PDF first."
        )

        st.stop()


    # -----------------------------
    # Display user question
    # -----------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    with st.chat_message("user"):

        st.markdown(question)


    # -----------------------------
    # Generate answer
    # -----------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Searching the PDF..."
        ):

            try:

                result = ask_question(
                    question,
                    st.session_state.vector_db,
                    st.session_state.llm
                )


                answer = result["answer"]

                sources = result["sources"]


                st.markdown(answer)


                if sources:

                    st.caption(
                        "Sources: "
                        + ", ".join(sources)
                    )


                # Store assistant response

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    }
                )


            except Exception as error:

                error_message = (
                    f"Error: {error}"
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                        "sources": []
                    }
                )