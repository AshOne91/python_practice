from http import client
from dotenv import load_dotenv
import os
import meilisearch

load_dotenv('.env', override=True)

client = meilisearch.Client(
    os.getenv("MEILI_SEARCH_URL"), 
    os.getenv("MEILI_SEARCH_KEY")
    )
def stock_search(query):
    return client.index("nasdaq").search(query)