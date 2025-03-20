import faiss

try:
    index = faiss.read_index("dataset/faiss_index_cleaned.bin")
    print("FAISS index loaded successfully!")
except Exception as e:
    print(f"Error loading FAISS index: {e}")
