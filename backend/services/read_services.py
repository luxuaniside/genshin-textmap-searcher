import os
from dotenv import load_dotenv
from supabase import create_client, Client


def search_query(query: str):
    load_dotenv()

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not url or not key:
        raise ValueError("SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY is missing from your .env file.")

    supabase: Client = create_client(url, key)

    try: 
        response = (
            supabase
            .rpc(
                "search_textmap",
                {
                    "search_query": query
                }
            )
            .execute()
        )

        return response.data if response.data else []

    except Exception as e:
        print(e)

        return None

