# scripts/run_query.py
from pathlib import Path

from docuagent.retrieval.hybrid_search import build_advanced_retriever
from dotenv import load_dotenv
from docuagent.retrieval.vector_store import ChromaRetriever
from docuagent.agent.rag_agent import RAGAgent

def main():
    # Load your GOOGLE_API_KEY from .env
    load_dotenv()
    
    print("Initializing AI Agent...")
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    db_path = project_root / "data" / "chroma_db"

    db_client = ChromaRetriever(db_dir=str(db_path))
    chroma_retriever = db_client.get_retriever(k=10)
    my_documents = db_client.get_all_document_chunks()

    if not my_documents:
        print("ERROR: Database is empty!")
        return

    advanced_retriever = build_advanced_retriever(
        chroma_retriever=chroma_retriever, 
        documents=my_documents,
        top_k=3 # Final chunks sent to Gemini
    )
    
    agent = RAGAgent( retriever=advanced_retriever)
    
    # 3. Start the chat loop
    print("\nAgent is ready! (Type 'exit' to stop)")
    while True:
        query = input("\nYour question: ")
        if query.lower() in ['exit', 'quit']:
            break
            
        answer = agent.ask(query)
        print(f"\nAI Answer:\n{answer}")

if __name__ == "__main__":
    main()