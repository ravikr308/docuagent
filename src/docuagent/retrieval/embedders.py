from langchain_google_genai import GoogleGenerativeAIEmbeddings

class EmbedderClient:
    """
    Manages the connection and configuration for the Gemini embedding model.
    """
    def __init__(self, model_name: str = "models/gemini-embedding-001"):
        self.model_name = model_name
        
    def get_model(self) -> GoogleGenerativeAIEmbeddings:
        # Returns the LangChain embedding object configured with the Gemini model
        return GoogleGenerativeAIEmbeddings(model=self.model_name)