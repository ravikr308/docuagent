from langchain_core.documents import Document

from .base import Chunker


class SemanticChunker_(Chunker):
    """Splits where embedding similarity between sentences drops.
    Costs one embedding call per sentence; keep only if your eval shows a win."""

    name = "semantic"

    def __init__(self, config, embeddings):
        super().__init__(config)
        from langchain_experimental.text_splitter import SemanticChunker

        self._splitter = SemanticChunker(
            embeddings,
            breakpoint_threshold_type="percentile",
            breakpoint_threshold_amount=config.semantic_percentile,
        )

    def split(self, docs: list[Document]) -> list[Document]:
        return self.enforce_max_size(self._splitter.split_documents(docs))