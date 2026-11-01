# CLI scripts for operational tasks (e.g., manual ingestion)

from dotenv import load_dotenv
from docuagent.ingestion.pipeline import IngestionPipeline

if __name__ == "__main__":
    load_dotenv() 
    
    pipeline = IngestionPipeline(
        data_dir="data/raw", 
        db_dir="data/chroma_db"
    )
    pipeline.run()