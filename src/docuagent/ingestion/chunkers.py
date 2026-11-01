from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from docuagent.core.logger import logger

def chunk_documents(
    documents: list[Document], 
    chunk_size: int = 1000, 
    chunk_overlap: int = 200
) -> list[Document]:
    """
    Splits a list of Documents into smaller chunks with semantic overlap.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""] # Tries to split on paragraphs first
    )
    
    chunked_docs = text_splitter.split_documents(documents)
    logger.info(f"Split documents into {len(chunked_docs)} chunks.")
    return chunked_docs