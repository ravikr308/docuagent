from langchain_chroma import Chroma

from docuagent.core.logger import logger
from docuagent.ingestion.chunking import ChunkingConfig, ChunkPostProcessor, build_chunker
from docuagent.ingestion.loaders import PDFLoader
from docuagent.retrieval.embedders import EmbedderClient


class IngestionPipeline:
    def __init__(self, data_dir: str, db_dir: str, config: ChunkingConfig | None = None):
        self.data_dir = data_dir
        self.db_dir = db_dir
        self.config = config or ChunkingConfig()
        self.embedder = EmbedderClient().get_model()

        self.loader = PDFLoader(as_markdown=self.config.strategy == "markdown")
        self.chunker = build_chunker(self.config, embeddings=self.embedder)
        self.postprocess = ChunkPostProcessor(self.config)

    def run(self) -> int:
        logger.info(f"Ingesting {self.data_dir} with strategy={self.config.strategy}")

        docs = self.loader.load_dir(self.data_dir)
        if not docs:
            logger.warning("No documents found.")
            return 0

        chunks = self.postprocess(self.chunker.split(docs))

        store = Chroma(embedding_function=self.embedder, persist_directory=self.db_dir)
        store.add_documents(chunks, ids=[c.metadata["chunk_id"] for c in chunks])  # upsert
        logger.info(f"Stored {len(chunks)} chunks.")
        return len(chunks)