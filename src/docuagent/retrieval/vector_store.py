# src/docugent/retrieval/vector_store.py
from langchain_chroma import Chroma
from docuagent.retrieval.embedders import EmbedderClient
from docuagent.core.logger import get_logger
from langchain_core.documents import Document

logger = get_logger(__name__)

class ChromaRetriever:
    def __init__(self, db_dir: str):
        self.embedder = EmbedderClient().get_model()
        self.db = Chroma(
            persist_directory=db_dir,
            embedding_function=self.embedder
        )
        logger.info(f"Connected to Chroma DB at {db_dir}")

    def get_retriever(self, k: int = 3):
        """
        Returns a retriever that fetches the top 'k' most similar chunks.
        """
        return self.db.as_retriever(search_kwargs={"k": k})

    def get_all_document_chunks(self):
        """Extracts existing raw text chunks directly from the Chroma DB."""
        print("Extracting existing text chunks from Chroma DB...")
        
        # Access the database using self.vectorstore
        db_data = self.db.get()
        
        document_chunks = []
        for text, metadata in zip(db_data['documents'], db_data['metadatas']):
            doc = Document(page_content=text, metadata=metadata)
            document_chunks.append(doc)
            
        print(f"Extracted {len(document_chunks)} chunks for BM25.")
        return document_chunks