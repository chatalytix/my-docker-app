import faiss
import numpy as np

def setup_faiss():
    """
    Initialize FAISS index with example data.
    """
    dimension = 128
    num_clusters = 10
    vectors = np.random.rand(100, dimension).astype('float32')  # Example data

    index = faiss.IndexFlatL2(dimension)  # Exact search
    ivf_index = faiss.IndexIVFFlat(index, dimension, num_clusters, faiss.METRIC_L2)
    ivf_index.train(vectors)  # Train with example data
    ivf_index.add(vectors)    # Add vectors to the index

    return ivf_index


def search_faiss(index, query_vector, top_k=5):
    """
    Perform FAISS vector search.
    """
    query = np.array([query_vector], dtype='float32')
    distances, indices = index.search(query, top_k)
    return [{"index": int(idx), "distance": float(dist)} for idx, dist in zip(indices[0], distances[0])]
