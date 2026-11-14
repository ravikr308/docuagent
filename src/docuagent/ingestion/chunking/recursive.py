from langchain_core.documents import Document

from .base import Chunker


class RecursiveChunker(Chunker):
    name = "recursive"

    def split(self, docs: list[Document]) -> list[Document]:
        return self.enforce_max_size(docs)