from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


@dataclass(frozen=True)
class ChunkingConfig:
    strategy: str = "markdown"          # recursive | markdown | semantic
    chunk_size: int = 1000
    chunk_overlap: int = 150
    min_chunk_chars: int = 80
    prepend_heading_path: bool = True
    semantic_percentile: float = 90.0


class Chunker(ABC):
    name: str

    def __init__(self, config: ChunkingConfig):
        self.config = config
        self._size_cap = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            add_start_index=True,
        )

    def enforce_max_size(self, docs: list[Document]) -> list[Document]:
        """Structure/semantic splits can be huge; guarantee a size ceiling."""
        return self._size_cap.split_documents(docs)

    @abstractmethod
    def split(self, docs: list[Document]) -> list[Document]: ...