from __future__ import annotations

from pathlib import Path

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document

from docuagent.core.logger import logger


class PDFLoader:
    """One Document per page. With as_markdown=True, headings become '#' markers."""

    def __init__(self, as_markdown: bool = True):
        self.as_markdown = as_markdown

    def load_file(self, path: Path) -> list[Document]:
        if self.as_markdown:
            import pymupdf4llm

            pages = pymupdf4llm.to_markdown(str(path), page_chunks=True)
            docs = [
                Document(
                    page_content=p["text"],
                    metadata={"source": str(path), "file_name": path.name, "page": i + 1},
                )
                for i, p in enumerate(pages)
            ]
        else:
            docs = PyMuPDFLoader(str(path)).load()
            for d in docs:
                d.metadata.update(source=str(path), file_name=path.name,
                                  page=d.metadata.get("page", 0) + 1)

        non_empty = [d for d in docs if d.page_content.strip()]
        if len(non_empty) < len(docs):
            logger.warning(f"{path.name}: {len(docs) - len(non_empty)} empty pages (scanned? needs OCR)")
        return non_empty

    def load_dir(self, data_dir: str | Path) -> list[Document]:
        root = Path(data_dir).resolve()
        if not root.is_dir():
            raise FileNotFoundError(f"Data directory not found: {root}")

        docs: list[Document] = []
        for pdf in sorted(root.rglob("*.pdf")):
            try:
                docs.extend(self.load_file(pdf))
            except Exception:
                logger.exception(f"Failed to load {pdf}")  # one bad PDF shouldn't kill the run
        logger.info(f"Loaded {len(docs)} pages from {root}")
        return docs