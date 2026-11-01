# scripts/run_query.py
from dotenv import load_dotenv
from docuagent.retrieval.vector_store import ChromaRetriever
from docuagent.agent.rag_agent import RAGAgent

def main():
    # Load your GOOGLE_API_KEY from .env
    load_dotenv()
    
    print("Initializing AI Agent...")
    # 1. Connect to the database
    db_client = ChromaRetriever(db_dir="data/chroma_db")
    retriever = db_client.get_retriever(k=3)
    
    # 2. Wire the database into the Agent
    agent = RAGAgent(retriever=retriever)
    
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