import pickle
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Indexer:
    def __init__(self, documents=None):
        self.documents = documents
        self.tf_idf_matrix = None
        self.vectorizer = TfidfVectorizer()

    def fit_transform(self):
        if self.documents is None:
            raise ValueError("No documents provided to index.")

        self.tf_idf_matrix = self.vectorizer.fit_transform(self.documents)

    def save_index(self, filename="index.pkl"):
        if self.tf_idf_matrix is None:
            raise ValueError("Index not yet created. Run fit_transform() first.")

        with open(filename, 'wb') as f:
            pickle.dump((self.vectorizer ,  self.tf_idf_matrix), f)

    def load_index(self, filename="index.pkl"):
        if not os.path.exists(filename):
            raise FileNotFoundError("Index file not found.")

        with open(filename, 'rb') as f:
            self.vectorizer, self.tf_idf_matrix = pickle.load(f)

    def search(self, query, top_n=5):
        if self.tf_idf_matrix is None:
            raise ValueError("Index not loaded. Load index using load_index() method.")

        query_vector = self.vectorizer.transform([query])
        cosine_similarities = cosine_similarity(query_vector, self.tf_idf_matrix)
        similarity_scores = cosine_similarities[0]
        top_indices = similarity_scores.argsort()[-top_n:][::-1]

        return [(idx, similarity_scores[idx]) for idx in top_indices]
    
def retrieve_all_documents(file_path):
    with open(file_path, 'rb') as f:
        all_documents = pickle.load(f)
    return all_documents


if __name__ == "__main__":    
    output_file = "all_documents.pkl"
    documents = retrieve_all_documents(output_file)
    
    indexer = Indexer(documents)
    indexer.fit_transform()
    indexer.save_index()
    print("Index created and saved successfully.")  