import os
import requests
from dotenv import load_dotenv
import time

# import re

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

"""
# Function to query Gemini API with a prompt and return the response
query_gemini(prompt: str) -> str:
This function sends a prompt to the Gemini API and returns the generated response.
"""
def query_gemini(prompt: str) -> str:
    headers = {"Content-Type": "application/json"}
    params = {"key": API_KEY}

    full_prompt = f"""
You are a helpful assistant.

Question:
{prompt}

Provide the most appropriate answer in **Most Precise Way eiter use table bullet point or what ever you fell is right if anything is not present in docs answer on your own**.
""".strip()

    data = {
        "contents": [
            {
                "parts": [{"text": full_prompt}]
            }
        ]
    }

    attempt = 1
    while True:
        response = requests.post(GEMINI_URL, headers=headers, params=params, json=data)
        try:
            response_json = response.json()
        except ValueError:
            return f"Invalid JSON response: {response.text}"

        if response.status_code == 200:
                try:
                    output = response_json['candidates'][0]['content']['parts'][0]['text']
                    return output.strip()
                except (KeyError, IndexError) as e:
                    return f"Malformed success response: {response_json}"
        elif response.status_code == 503:
                print(f"[Retry {attempt}] Gemini is overloaded. Retrying...")
                time.sleep(2 + attempt)
                attempt += 1
        else:
                return f"Error {response.status_code}: {response.text}"

    
if __name__ == "__main__":
    response = query_gemini("How to make chicken biryani?")
    print(response)
    

