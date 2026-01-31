import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY environment variable not set")
    print("Make sure you have a .env file with GEMINI_API_KEY")
    exit(1)

# Use the REST API to list models
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    if "models" in data:
        print(f"Found {len(data['models'])} models:\n")
        for model in data["models"]:
            name = model.get("name", "Unknown")
            display_name = model.get("displayName", "")
            methods = model.get("supportedGenerationMethods", [])
            print(f"Model name: {name}")
            print(f"  Display name: {display_name}")
            print(f"  Supported methods: {methods}")
            print("-" * 60)
    else:
        print("No models found in response")
        print(data)
except requests.exceptions.RequestException as e:
    print(f"Error fetching models: {e}")
