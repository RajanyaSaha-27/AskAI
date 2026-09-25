# 📚 PDF RAG Assistant

A **Retrieval-Augmented Generation (RAG)** application that allows users to upload a PDF and ask questions about its content through an interactive **Streamlit** interface.

The system retrieves relevant information from the uploaded document and uses **Google Gemini** to generate grounded answers based only on the retrieved content.

---

## 🚀 Features

* 📄 Upload PDF documents directly through the UI
* ✂️ Split documents using `RecursiveCharacterTextSplitter`
* 🧠 Generate semantic embeddings using `GoogleGenerativeAIEmbeddings`
* 🗄️ Store document vectors using `ChromaDB`
* 🔎 Retrieve the most relevant document chunks for a query
* 🤖 Generate answers using `Gemini`
* 💬 Interactive chat interface with Streamlit
* 📖 Display source page numbers for retrieved information
* 🔒 Answers are restricted to the uploaded PDF context to reduce hallucination

---

## 🛠️ Tech Stack

* **Python**
* **Streamlit** — Frontend/UI
* **LangChain** — RAG pipeline
* **PyPDF** — PDF document loading
* **RecursiveCharacterTextSplitter** — Text chunking
* **GoogleGenerativeAIEmbeddings** — Text embeddings
* **ChromaDB** — Vector database
* **Google Gemini** — Answer generation
* **python-dotenv** — Environment variable management

---

## 📂 Project Structure

```text
RAG/
│
├── document_loaders/
│   └── pdf_loader.py
│
├── .env
├── app.py
├── create_chroma.py
├── embedding.py
├── main.py
└── README.md
```

---

## 🔄 How It Works

```text
                PDF Upload
                    │
                    ▼
             PDF Document Loader
                    │
                    ▼
       RecursiveCharacterTextSplitter
                    │
                    ▼
          Document Chunks
                    │
                    ▼
       Google Generative AI Embeddings
                    │
                    ▼
               ChromaDB
                    │
                    │
             User Question
                    │
                    ▼
           Similarity Retrieval
                    │
                    ▼
          Relevant PDF Chunks
                    │
                    ▼
             Google Gemini
                    │
                    ▼
             Grounded Answer
                    │
                    ▼
             Streamlit UI
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd RAG
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it.

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install the required dependencies:

```bash
pip install streamlit
pip install langchain
pip install langchain-community
pip install langchain-google-genai
pip install langchain-chroma
pip install langchain-text-splitters
pip install pypdf
pip install python-dotenv
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key
```

Replace `your_google_api_key` with your Google AI API key.

**Never commit your `.env` file or API key to GitHub.**

---

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

Streamlit will open the application in your browser.

---

## 📖 Usage

### 1. Upload a PDF

Use the **Upload PDF** section to select your document.

### 2. Process the PDF

Click:

```text
🚀 Process PDF
```

The application will:

1. Load the PDF
2. Extract its text
3. Split the text into chunks
4. Generate embeddings
5. Store the embeddings in ChromaDB

### 3. Ask Questions

After processing, enter your question in the chat box.

For example:

```text
What is the main objective of this paper?
```

The system retrieves relevant sections from the PDF and sends them as context to Gemini.

### 4. View Sources

The application also displays the relevant **PDF page numbers** used to generate the answer.

---

## 🧩 RAG Pipeline

The project follows the standard RAG architecture:

### 1. Retrieval

The user's question is converted into an embedding and compared with the document embeddings stored in ChromaDB.

### 2. Context Selection

The most relevant document chunks are retrieved using similarity search.

### 3. Generation

The retrieved chunks are provided as context to Gemini, which generates the final response.

This allows the application to answer questions based on the uploaded document rather than relying solely on the model's general knowledge.

---

## 🛡️ Hallucination Control

The prompt instructs the model to:

* Use only the retrieved PDF context
* Avoid using outside information
* Avoid making up information
* Clearly state when the requested information cannot be found in the document

This helps keep responses grounded in the source document.

---

## 📌 Current Limitations

* One uploaded PDF is processed for the current session.
* Conversation history is maintained in the Streamlit session.
* Retrieval currently uses a fixed number of relevant chunks.
* The system does not yet provide advanced retrieval evaluation.
* Very large documents may require further optimization for chunking and retrieval.

---

## 🔮 Future Improvements

* Support multiple PDFs simultaneously
* Persistent document storage
* Conversational memory across sessions
* Improved retrieval and reranking
* Hybrid search
* Retrieval evaluation metrics
* Better source citations with highlighted passages
* Streaming responses
* Document management and deletion
* Support for additional document formats such as DOCX and TXT
* Authentication and user-specific document collections

---

## 📄 License

This project is intended for educational and experimental purposes.
