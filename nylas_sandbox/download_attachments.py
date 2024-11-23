from dotenv import load_dotenv
import os
from nylas import Client
import json

def download_attachments(message_id, attachment_id):
  nylas = Client(
        api_key=os.environ['NYLAS_API_KEY'],
        api_uri=os.environ['NYLAS_API_URI']
    )
  grant_id = os.environ.get("TEST_GRANT_ID")
  if not grant_id:
    raise ValueError("TEST_GRANT_ID is not set")
  
  query_params = {"message_id": message_id}
  try:
    # First, get attachment metadata to get the filename
    attachment_info = nylas.attachments.find(grant_id, attachment_id, query_params)
    filename = attachment_info.data.filename  # Get original filename
    
    # Download the attachment bytes
    attachment_bytes = nylas.attachments.download_bytes(
        grant_id, 
        attachment_id,
        query_params
    )
    
    # Write bytes to file with original filename
    with open(filename, 'wb') as f:
        f.write(attachment_bytes)
    
    return f"Saved attachment as: {filename}"
  except Exception as e:
    return f'{e}'
  
attachment_id = os.environ["TEST_ATTACHMENT_ID"]
message_id = os.environ["TEST_MESSAGE_ID"]

attachment = download_attachments(message_id, attachment_id)

print(attachment)

