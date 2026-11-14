from __future__ import annotations

from collections import defaultdict

from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter

from .base import Chunker

LEVELS = ("h1", "h2", "h3")


def _with_inherited_headers(meta: dict, carried: dict) -> dict:
    """A page often starts mid-section; inherit parent headings from the previous page."""
    own = [i for i, k in enumerate(LEVELS) if k in meta]
    if not own:
        return {**carried, **meta}
    inherited = {k: carried[k] for k in LEVELS[: own[0]] if k in carried}
    return {**inherited, **meta}


class MarkdownChunker(Chunker):
    name = "markdown"

    def __init__(self, config):
        super().__init__(config)
        self._header_splitter = MarkdownHeaderTextSplitter(
            [("#", "h1"), ("##", "h2"), ("###", "h3")], strip_headers=False
        )

    def split(self, docs: list[Document]) -> list[Document]:
        by_source: dict[str, list[Document]] = defaultdict(list)
        for d in docs:
            by_source[d.metadata.get("source", "unknown")].append(d)

        sections: list[Document] = []
        for pages in by_source.values():
            carried: dict = {}
            for page in sorted(pages, key=lambda p: p.metadata.get("page", 0)):
                for sec in self._header_splitter.split_text(page.page_content):
                    headers = _with_inherited_headers(sec.metadata, carried)
                    carried = {k: headers[k] for k in LEVELS if k in headers}
                    sections.append(
                        Document(
                            page_content=sec.page_content,
                            metadata={**page.metadata, **headers},
                        )
                    )
        return self.enforce_max_size(sections)