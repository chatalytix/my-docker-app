from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["faiss_database"]
metadata_collection = db["items"]

# Insert sample metadata
sample_metadata = [
    {"index": 0, "item_name": "Free Product A", "is_free": True, "category": "Gadgets"},
    {"index": 1, "item_name": "Paid Product B", "is_free": False, "category": "Accessories"},
    {"index": 2, "item_name": "Free Product C", "is_free": True, "category": "Books"},
]

metadata_collection.insert_many(sample_metadata)
print("Sample data inserted!")
