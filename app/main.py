# File: app/main.py

from fastapi import FastAPI, HTTPException
import faiss
import numpy as np
from pydantic import BaseModel

app = FastAPI()

# Define a basic FAISS index
dimension = 128  # Vector dimension
index = faiss.IndexFlatL2(dimension)  # L2 distance index

# Example vector store (for in-memory)
vectors_store = {}

class VectorData(BaseModel):
    id: str
    vector: list[float]

class QueryData(BaseModel):
    vector: list[float]
    top_k: int

@app.post("/add-vector/")
def add_vector(data: VectorData):
    """Add a vector to the FAISS index."""
    if data.id in vectors_store:
        raise HTTPException(status_code=400, detail="ID already exists.")
    
    vector = np.array(data.vector, dtype='float32')
    if len(vector) != dimension:
        raise HTTPException(status_code=400, detail=f"Vector must have {dimension} dimensions.")

    index.add(vector.reshape(1, -1))
    vectors_store[data.id] = vector
    return {"message": "Vector added successfully."}

@app.post("/search/")
def search_vector(data: QueryData):
    """Search for the closest vectors."""
    query = np.array(data.vector, dtype='float32')
    if len(query) != dimension:
        raise HTTPException(status_code=400, detail=f"Query vector must have {dimension} dimensions.")

    if data.top_k <= 0:
        raise HTTPException(status_code=400, detail="top_k must be greater than 0.")
    
    distances, indices = index.search(query.reshape(1, -1), data.top_k)
    results = [{"id": list(vectors_store.keys())[i], "distance": distances[0][i]} for i in indices[0] if i < len(vectors_store)]

    return {"results": results}

@app.get("/")
def root():
    return {"message": "FAISS API is running!"}
