from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not url or not key:
    raise ValueError("SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY is missing from your .env file.")

supabase: Client = create_client(url, key)


from tqdm import tqdm

def upload_data(data):
    BATCH_SIZE = 1000
    total = len(data)

    for i in tqdm(range(0, total, BATCH_SIZE), desc="Uploading"):
        batch = data[i:i + BATCH_SIZE]

        supabase.table("textmap").upsert(batch).execute()

