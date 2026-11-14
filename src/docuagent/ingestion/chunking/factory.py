from __future__ import annotations

from .base import Chunker, ChunkingConfig
from .markdown import MarkdownChunker
from .recursive import RecursiveChunker
from .semantic import SemanticChunker_


def build_chunker(config: ChunkingConfig, embeddings=None) -> Chunker:
    match config.strategy:
        case "recursive":
            return RecursiveChunker(config)
        case "markdown":
            return MarkdownChunker(config)
        case "semantic":
            if embeddings is None:
                raise ValueError("semantic strategy requires an embeddings model")
            return SemanticChunker_(config, embeddings)
        case other:
            raise ValueError(f"Unknown chunking strategy: {other!r}")