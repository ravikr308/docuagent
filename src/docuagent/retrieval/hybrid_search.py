# src/docuagent/retrieval/hybrid_search.py
from langchain_classic.retrievers import EnsembleRetriever, ContextualCompressionRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from docuagent.core.logger import get_logger

logger = get_logger(__name__)

def build_advanced_retriever(chroma_retriever, documents, top_k=3):
    """
    Builds a Hybrid (BM25 + Chroma) retriever wrapped with a Cross-Encoder Reranker.
    """
    logger.info("Building BM25 Retriever...")
    bm25_retriever = BM25Retriever.from_documents(documents)
    bm25_retriever.k = 10 
    
    logger.info("Combining into Ensemble Retriever...")
    hybrid_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, chroma_retriever],
        weights=[0.5, 0.5] 
    )
    
    # logger.info("Loading HuggingFace Reranker model...")
    # reranker_model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-v2-m3")
    
    # # Filter down to the absolute best `top_k` documents
    # compressor = CrossEncoderReranker(model=reranker_model, top_n=top_k)
    
    # logger.info("Wrapping with Contextual Compression...")
    # final_retriever = ContextualCompressionRetriever(
    #     base_compressor=compressor,
    #     base_retriever=hybrid_retriever
    # )
    
    return hybrid_retriever