# scripts/check_models.py
import os
from dotenv import load_dotenv
from google import genai

def list_my_models():
    load_dotenv()
    
    # Initialize the client using your GOOGLE_API_KEY
    client = genai.Client(api_key=os.environ.get('GOOGLE_API_KEY'))
    
    print("--- Active Models For My API Key ---")
    
    # Fetch and print all models without filtering
    for model in client.models.list():
        print(model.name)

if __name__ == "__main__":
    list_my_models()