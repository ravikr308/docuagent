from __future__ import annotations

import hashlib

from langchain_core.documents import Document

from docuagent.core.logger import logger

from .base import ChunkingConfig

LEVELS = ("h1", "h2", "h3")


def _clean_metadata(meta: dict) -> dict:
    """Chroma only accepts str/int/float/bool values."""
    return {
        k: v for k, v in meta.items()
        if isinstance(v, (str, int, float, bool))
    }


class ChunkPostProcessor:
    def __init__(self, config: ChunkingConfig):
        self.config = config

    def __call__(self, chunks: list[Document]) -> list[Document]:
        seen: set[str] = set()
        out: list[Document] = []

        for c in chunks:
            text = c.page_content.strip()
            if len(text) < self.config.min_chunk_chars:
                continue

            meta = c.metadata
            chunk_id = hashlib.sha1(
                f"{meta.get('source')}|{meta.get('page')}|{text}".encode()
            ).hexdigest()
            if chunk_id in seen:
                continue
            seen.add(chunk_id)

            path = " > ".join(meta[k] for k in LEVELS if meta.get(k))
            meta = _clean_metadata(meta)
            meta.update(
                chunk_id=chunk_id,
                chunk_index=len(out),
                heading_path=path,
                char_count=len(text),
                strategy=self.config.strategy,
            )
            content = (
                f"[{path}]\n{text}"
                if path and self.config.prepend_heading_path
                else text
            )
            out.append(Document(page_content=content, metadata=meta))

        logger.info(f"Post-processing: {len(chunks)} -> {len(out)} chunks")
        return out