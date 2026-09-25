import os

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()


def create_llm():

    google_api_key = os.getenv("GOOGLE_API_KEY")

    if not google_api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found in .env file."
        )

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        temperature=0.2,
        google_api_key=google_api_key
    )

    return llm


def ask_question(question, vector_db, llm):

    # -----------------------------
    # Retrieve relevant documents
    # -----------------------------

    retriever = vector_db.as_retriever(
        search_kwargs={
            "k": 4
        }
    )

    relevant_documents = retriever.invoke(question)


    if not relevant_documents:

        return {
            "answer": "I could not find relevant information in the uploaded PDF.",
            "sources": []
        }


    # -----------------------------
    # Build context
    # -----------------------------

    context = "\n\n".join(
        document.page_content
        for document in relevant_documents
    )


    # -----------------------------
    # Prompt Gemini
    # -----------------------------

    prompt = f"""
You are a PDF question-answering assistant.

Answer the user's question using ONLY the provided context.

Rules:
1. Do not use outside knowledge.
2. Do not make up information.
3. If the answer cannot be found in the context,
   clearly say that the information is not available
   in the uploaded PDF.
4. Give a clear and concise answer.

Context:
{context}

Question:
{question}

Answer:
"""


    response = llm.invoke(prompt)


    # -----------------------------
    # Extract source information
    # -----------------------------

    sources = []

    for document in relevant_documents:

        page = document.metadata.get("page")

        if page is not None:

            page_number = page + 1

            source = f"Page {page_number}"

        else:

            source = "Unknown page"


        if source not in sources:

            sources.append(source)


    return {
        "answer": response.content[0]['text'],
        "sources": sources
    }