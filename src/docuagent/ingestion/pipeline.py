from langchain_chroma import Chroma

from docuagent.ingestion.loaders import load_documents_from_dir
from docuagent.ingestion.chunkers import chunk_documents

from docuagent.retrieval.embedders import EmbedderClient
from docuagent.core.logger import logger

class IngestionPipeline:
    def __init__(self, data_dir: str, db_dir: str):
        self.data_dir = data_dir
        self.db_dir = db_dir
        self.embedder = EmbedderClient().get_model()

    def run(self):
        logger.info(f"Starting ingestion from {self.data_dir}...")
        
        # 1. Transform Data
        raw_docs = load_documents_from_dir(self.data_dir)
        if not raw_docs:
            logger.warning("No documents found.")
            return
            
        chunks = chunk_documents(raw_docs)
        
        # 2. Store Data
        logger.info("Embedding and saving chunks to Vector DB...")
        Chroma.from_documents(
            documents=chunks,
            embedding=self.embedder,
            persist_directory=self.db_dir
        )
        logger.info("Pipeline finished successfully.")