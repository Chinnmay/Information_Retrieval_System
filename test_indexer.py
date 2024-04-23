import os
import pickle
import pytest
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from indexer import Indexer, retrieve_all_documents

# Define fixture to prepare test data
@pytest.fixture
def sample_documents():
    documents = [
        "This is document 1",
        "Another document here",
        "And one more document"
    ]
    with open("test_documents.pkl", "wb") as f:
        pickle.dump(documents, f)
    return "test_documents.pkl"

# Test case to check if Indexer instance is created properly
def test_indexer_instance(sample_documents):
    documents = retrieve_all_documents(sample_documents)
    indexer = Indexer(documents)
    assert isinstance(indexer, Indexer)

# Test case to check if fit_transform() method works correctly
def test_fit_transform(sample_documents):
    documents = retrieve_all_documents(sample_documents)
    indexer = Indexer(documents)
    indexer.fit_transform()
    assert indexer.tf_idf_matrix is not None

# Test case to check if save_index() method works correctly
def test_save_index(sample_documents):
    documents = retrieve_all_documents(sample_documents)
    indexer = Indexer(documents)
    indexer.fit_transform()
    indexer.save_index("test_index.pkl")
    assert os.path.exists("test_index.pkl")

# Test case to check if load_index() method works correctly
def test_load_index(sample_documents):
    documents = retrieve_all_documents(sample_documents)
    indexer = Indexer(documents)
    indexer.fit_transform()
    indexer.save_index("test_index.pkl")

    loaded_indexer = Indexer()
    loaded_indexer.load_index("test_index.pkl")
    assert loaded_indexer.tf_idf_matrix is not None

# Cleanup test files
def teardown_module(module):
    os.remove("test_documents.pkl")
    os.remove("test_index.pkl")
