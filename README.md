# 📄 DocuAgent

### Intelligent Document Q&A Powered by Retrieval-Augmented Generation (RAG)

**DocuAgent** is an open-source, RAG-powered platform that transforms unstructured documents into an intelligent question-answering system. It enables users to interact with their internal knowledge base using natural language and receive context-aware responses grounded in their source documents.

Instead of relying entirely on an LLM's pretrained knowledge, DocuAgent retrieves relevant information from a vector database and uses that context to generate more accurate and reliable answers.

---

## ✨ Key Features

- **📂 Automated Document Ingestion:** Processes unstructured files, including PDFs, Markdown, text files, and logs.
- **🧠 Retrieval-Augmented Generation:** Combines semantic search with LLM-powered response generation.
- **🔍 Semantic Search:** Retrieves relevant document chunks using vector embeddings and similarity search.
- **📚 Context-Aware Responses:** Generates answers based on retrieved document context rather than relying solely on generic LLM knowledge.
- **🛡️ Grounded Answering:** Designed to avoid unsupported responses when relevant information is unavailable in the knowledge base.
- **⚡ Efficient Processing:** Uses document chunking and embedding pipelines to prepare information for retrieval.
- **🐍 Modern Python Tooling:** Uses `uv` for fast dependency management and environment setup.

---

## 🏗️ Architecture Overview

DocuAgent follows a modular RAG architecture with two primary workflows:

**1. Document Ingestion Pipeline**

Raw Documents → Document Loading → Text Cleaning → Chunking → Embedding Generation → ChromaDB

**2. Query & Retrieval Pipeline**

User Query → Semantic Retrieval → Relevant Context → LLM → Context-Aware Answer

---

## 📁 Project Structure

```text
docuagent/
│
├── data/
│   ├── raw/                       # Original documents (PDF, TXT, MD)
│   └── chroma_db/                 # Persistent vector database
│
├── scripts/
│   ├── run_ingestion.py           # Document ingestion entry point
│   └── run_query.py               # Interactive Q&A entry point
│
├── docuagent/
│   ├── ingestion/
│   │   └── pipeline.py            # Document processing pipeline
│   │
│   ├── retrieval/
│   │   └── vector_store.py        # ChromaDB retriever
│   │
│   └── agent/
│       └── rag_agent.py           # RAG agent implementation
│
├── requirements.txt               # Python dependencies
├── pyproject.toml                 # Project configuration
├── .env                           # Environment variables
├── .gitignore                     # Git ignored files
└── README.md                      # Project documentation
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| RAG | Retrieval-Augmented Generation |
| Google Gemini | LLM-powered response generation |
| ChromaDB | Vector storage and similarity search |
| Embeddings | Semantic document representation |
| LangChain (if used) | Document processing and retrieval integration |
| uv | Python package and environment management |
| python-dotenv | Environment variable management |

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)
- Google Gemini API Key

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/docuagent.git

cd docuagent
```

### 2. Initialize the Environment

Install the project dependencies:

```bash
uv init

uv pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

**Important:** Never commit your API keys or other sensitive credentials to GitHub.

Add the following to `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
*.pyc
data/chroma_db/
```

### 4. Add Your Documents

Place your documents inside the raw data directory.

```text
data/
└── raw/
    ├── company_policy.pdf
    ├── technical_documentation.pdf
    ├── project_notes.md
    └── application_logs.txt
```

---

## ⚙️ Running the Application

### Step 1: Document Ingestion

The ingestion pipeline loads documents, processes their content, generates embeddings, and stores the resulting vectors in ChromaDB.

Create `scripts/run_ingestion.py`:

```python
from dotenv import load_dotenv
from docuagent.ingestion.pipeline import IngestionPipeline


if __name__ == "__main__":
    load_dotenv()

    pipeline = IngestionPipeline(
        data_dir="data/raw",
        db_dir="data/chroma_db"
    )

    pipeline.run()
```

Run the ingestion pipeline:

```bash
uv run python scripts/run_ingestion.py
```

Once completed, your document embeddings will be stored in the local ChromaDB database.

### Step 2: Query Your Documents

After ingestion, you can start interacting with your documents through the RAG agent.

Create `scripts/run_query.py`:

```python
from dotenv import load_dotenv

from docuagent.retrieval.vector_store import ChromaRetriever
from docuagent.agent.rag_agent import RAGAgent


def main():
    load_dotenv()

    print("Initializing DocuAgent...")

    # Connect to the vector database
    db_client = ChromaRetriever(
        db_dir="data/chroma_db"
    )

    # Retrieve the top 3 relevant document chunks
    retriever = db_client.get_retriever(k=3)

    # Initialize the RAG agent
    agent = RAGAgent(retriever=retriever)

    print("\nDocuAgent is ready!")
    print("Ask questions about your documents.")
    print("Type 'exit' or 'quit' to stop.")

    while True:
        query = input("\nYou: ").strip()

        if query.lower() in ["exit", "quit"]:
            print("Exiting DocuAgent. Goodbye!")
            break

        if not query:
            continue

        answer = agent.ask(query)

        print(f"\nDocuAgent:\n{answer}")


if __name__ == "__main__":
    main()
```

Run the query application:

```bash
uv run python scripts/run_query.py
```

### Step 3: Ask Questions

Once the agent starts, you can ask questions based on the documents you uploaded.

**Example:**

```text
Initializing DocuAgent...

DocuAgent is ready!
Ask questions about your documents.

You: What is the company's leave policy?

DocuAgent:
Based on the uploaded company policy document,
employees are entitled to...

You: What is the procedure for requesting leave?

DocuAgent:
According to the retrieved documentation...

You: exit

Exiting DocuAgent. Goodbye!
```

*Note: The answers above are illustrative examples. Actual responses depend on the documents in your knowledge base.*

---

## 🔄 How It Works

| Component | Responsibility |
|---|---|
| Document Loader | Extracts content from different file formats |
| Text Processor | Cleans and prepares extracted content |
| Chunking | Splits large documents into smaller segments |
| Embedding Model | Converts text into numerical vector representations |
| ChromaDB | Stores and indexes document embeddings |
| Retriever | Finds the most relevant document chunks |
| RAG Agent | Combines retrieved context with the user query |
| LLM | Generates a natural-language response |

---

## 🗺️ Future Enhancements

- [ ] Support additional document formats such as DOCX and CSV.
- [ ] Add source citations and document references to generated answers.
- [ ] Implement conversation history and multi-turn conversations.
- [ ] Add metadata filtering for document retrieval.
- [ ] Introduce hybrid search (semantic + keyword search).
- [ ] Build a React-based chat interface.
- [ ] Add authentication and multi-user document isolation.
- [ ] Containerize the application using Docker.
- [ ] Implement evaluation metrics for retrieval quality and answer accuracy.
- [ ] Add document upload and management APIs.

---

## 🤝 Contributing

Contributions are welcome!

If you would like to improve DocuAgent:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push your branch.
5. Open a Pull Request.

For major changes, please open an issue first to discuss your proposed improvements.

---

## 📄 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for more information.

---

## 👨‍💻 Author

**Ravi Kumar**

- GitHub: [@ravikr309](https://github.com/ravikr308)
- LinkedIn: [Ravi Kumar](https://www.linkedin.com/in/ravikumar309/)

---

⭐ If you find DocuAgent useful, consider giving the repository a star!

**DocuAgent — Turn your documents into knowledge.**
