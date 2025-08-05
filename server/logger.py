import json
from datetime import datetime
import os

# Create logs directory if it doesn't exist
log_dir = os.path.join(os.path.dirname(__file__), '..', 'server', 'logs')
os.makedirs(log_dir, exist_ok=True)

log_file_path = os.path.join(log_dir, 'query_log.jsonl')

def log_interaction(prompt: str, response: str):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "response": response,
        "model": "gemini-2.0-flash"
    }

    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(json.dumps(entry) + "\n")

