from pathlib import Path
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from docuagent.core.logger import logger

def load_documents_from_dir(data_dir: str | Path) -> list[Document]:
    """
    Scans a directory for PDF files and loads their text and metadata.
    """
    directory_path = Path(data_dir)
    documents: list[Document] = []
    
    # Iterate through all PDFs in the directory
    for pdf_path in directory_path.rglob("*.pdf"):
        loader = PyMuPDFLoader(str(pdf_path))
        documents.extend(loader.load())
        
    logger.info(f"Loaded {len(documents)} pages from {data_dir}")
    return documents