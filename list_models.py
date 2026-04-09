import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
r = requests.get(f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}")
data = r.json()
print("\n".join([m["name"] for m in data.get("models", []) if "gemini" in m["name"]]))
