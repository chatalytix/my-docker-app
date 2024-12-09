from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection setup
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

# Specify the database and collection
db = client["faiss_database"]
metadata_collection = db["items"]

def get_metadata(search_results):
    """
    Enrich FAISS search results with metadata from MongoDB.
    """
    enriched_results = []
    for result in search_results:
        metadata = metadata_collection.find_one({"index": result["index"]})
        if metadata:
            enriched_results.append({**result, **metadata})
    return enriched_results
