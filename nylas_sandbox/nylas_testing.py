from dotenv import load_dotenv
import os
from nylas import Client
from nylas.models.messages import ListMessagesQueryParams
import json

load_dotenv(override=True)

JSON_PATH = "data.json"

def recent_emails():
    nylas = Client(
        api_key=os.environ['NYLAS_API_KEY'],
        api_uri=os.environ['NYLAS_API_URI']
    )
    grant_id = os.environ.get("TEST_GRANT_ID")
    if not grant_id:
        raise ValueError("TEST_GRANT_ID is not set")

    query_params = {"limit": 1}

    try:
        messages, _, _ = nylas.messages.list(
            grant_id, 
            query_params
        )

        return messages
    except Exception as e:
        return f'{e}'   
  
def dump_to_json(messages):
    # Write each message to a new line in the JSON Lines format
    with open(JSON_PATH, 'w') as f:
        for message in messages:
            f.write(message.to_json() + '\n')  # Write each message as a separate line

def pretty_print_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)  # Load the JSON data

    pretty_json = json.dumps(data, indent=4)  # Pretty print with 4 spaces indentation

    with open(file_path, 'w') as f:
        f.write(pretty_json)  # Write the pretty printed JSON back to the file

emails = recent_emails()
dump_to_json(emails)
pretty_print_json(JSON_PATH)
