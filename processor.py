from flask import Flask, request, jsonify
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# python app.py
# curl -X POST -H "Content-Type: application/json" -d '{"query": "information retrieval system", "top_k": 3}' http://localhost:5000/process_query


# Load the inverted index
with open('index.pkl', 'rb') as f:
    inverted_index = pickle.load(f)

# Load the documents
with open('documents.pkl', 'rb') as f:
    documents = pickle.load(f)

# Initialize Flask app
app = Flask(__name__)

# Define function to process queries
def process_query(query, top_k=5):
    # Validate query
    if not query:
        return jsonify({"error": "Empty query"})

    # Vectorize the query
    vectorizer = TfidfVectorizer(vocabulary=inverted_index.keys())
    query_vector = vectorizer.fit_transform([query])

    # Calculate cosine similarity between query and documents
    similarity_scores = cosine_similarity(query_vector, list(inverted_index.values()))

    # Get top-K ranked results
    top_results_indices = similarity_scores.argsort()[0][-top_k:][::-1]
    top_results = [(documents[idx], similarity_scores[0][idx]) for idx in top_results_indices]

    return top_results

# Define route for query processing
@app.route('/process_query', methods=['POST'])
def process_query_route():
    data = request.get_json()
    query = data.get('query')
    top_k = data.get('top_k', 5)  # Default to top 5 results if top_k not specified

    results = process_query(query, top_k)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
