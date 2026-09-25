from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from embedding import get_embedding_model


def create_vector_database(documents):

    # -----------------------------
    # Split documents into chunks
    # -----------------------------

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks.")


    # -----------------------------
    # Create embedding model
    # -----------------------------

    embedding_model = get_embedding_model()


    # -----------------------------
    # Create Chroma vector database
    # -----------------------------

    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model
    )

    print("Chroma vector database created successfully.")

    return vector_db