# CLI scripts for operational tasks (e.g., manual ingestion)

from anyio import Path
from dotenv import load_dotenv
from docuagent.ingestion.pipeline import IngestionPipeline

if __name__ == "__main__":
    load_dotenv() 

    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    data_path = project_root / "data" / "raw"
    db_path = project_root / "data" / "chroma_db"

    
    pipeline = IngestionPipeline(
        data_dir=str(data_path),
        db_dir=str(db_path)
    )
    pipeline.run()