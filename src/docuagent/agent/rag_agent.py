import os

from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from docuagent.core.logger import get_logger

logger = get_logger(__name__)

class RAGAgent:
    def __init__(self, retriever):
        
        raw_client = genai.Client(
            api_key=os.environ.get('GOOGLE_API_KEY'),
            http_options={'api_version': 'v1alpha'}
        )
        
        # 2. Pass the raw client directly into LangChain
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.8-flash", 
            client=raw_client,
            temperature=0.1
        )

        self.retriever = retriever
        
        system_prompt = (
            "You are an intelligent assistant. Use the following pieces of retrieved "
            "context to answer the user's question. If you don't know the answer, "
            "just say that you don't know. Keep the answer concise and accurate.\n\n"
            "Context:\n{context}"
        )
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}")
        ])
        
        self.qa_chain = create_stuff_documents_chain(self.llm, self.prompt)
        self.rag_chain = create_retrieval_chain(self.retriever, self.qa_chain)
        logger.info("RAG Agent initialized.")

    def ask(self, query: str):
        for chunk in self.rag_chain.stream({"input": query}):
            if "answer" in chunk:
                print(chunk["answer"], end="", flush=True)
        print()