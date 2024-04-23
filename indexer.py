import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Indexer:
    def __init__(self, documents=None):
        self.documents = documents
        self.tf_idf_matrix = None
        self.vectorizer = TfidfVectorizer()

    # Fit the vectorizer and transform the documents
    def fit_transform(self):
        if self.documents is None:
            raise ValueError("No documents provided to index.")
        self.tf_idf_matrix = self.vectorizer.fit_transform(self.documents)

    # Save the vectorizer and tf-idf matrix to a file
    def save_index(self, filename="index.pkl"):
        if self.tf_idf_matrix is None:
            raise ValueError("Index not yet created. Run fit_transform() first.")

        with open(filename, 'wb') as f:
            pickle.dump((self.vectorizer ,  self.tf_idf_matrix), f)

    # Load the vectorizer and tf-idf matrix from a file
    def load_index(self, filename="index.pkl"):
        if not os.path.exists(filename):
            raise FileNotFoundError("Index file not found.")
        with open(filename, 'rb') as f:
            self.vectorizer, self.tf_idf_matrix = pickle.load(f)
    
# Load the documents from the file
def retrieve_all_documents(file_path):
    with open(file_path, 'rb') as f:
        all_documents = pickle.load(f)
    return all_documents

if __name__ == "__main__":    
    output_file = "all_documents.pkl"
    # Example usage to create an index
    documents = retrieve_all_documents(output_file)
    # Create an indexer object
    indexer = Indexer(documents)
    indexer.fit_transform()
    indexer.save_index()
    print("Index created and saved successfully.")  