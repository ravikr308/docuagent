# src/docugent/retrieval/vector_store.py
from langchain_chroma import Chroma
from docuagent.retrieval.embedders import EmbedderClient
from docuagent.core.logger import get_logger

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