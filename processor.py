from flask import Flask, render_template, request, jsonify
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# python app.py
# curl -X POST -H "Content-Type: application/json" -d '{"query": "information retrieval system", "top_k": 3}' http://localhost:5000/process_query


# Load the inverted index
with open('index.pkl', 'rb') as f:
    vectorizer, tf_idf_matrix = pickle.load(f)

# Load the documents
with open('all_documents.pkl', 'rb') as f:
    documents = pickle.load(f)

# Initialize Flask app
app = Flask(__name__)

# Define function to process queries
def process_query(query, top_k=5):
    # Validate query
    if not query:
        return jsonify({"error": "Empty query"})
    # Vectorize the query
    query_vector = vectorizer.transform([query])
    # Calculate cosine similarity between query and documents
    similarity_scores = cosine_similarity(query_vector, tf_idf_matrix)
    
    # Get top-K ranked results
    top_results_indices = similarity_scores.argsort()[0][-top_k:][::-1]
    top_results = [(str(documents[idx]).split('\n')[0], similarity_scores[0][idx]) for idx in top_results_indices]
    return top_results

def validate_query(query_data):
    # Check if query data is provided
    if not query_data:
        return False, "Empty query data. Please provide a valid JSON object."
    # Check if 'query' field is present
    if 'query' not in query_data:
        return False, "Missing 'query' field in the JSON object."
    # Check if 'query' field is empty
    if not query_data['query']:
        return False, "Empty query. Please provide a valid query."
    # Add more validation checks as needed
    return True, "Query validated successfully."

# Define route for home page
@app.route('/')
def home():
    return render_template('index.html')

# Define route for query processing
@app.route('/process_query', methods=['POST'])
def process_query_route():
    """data = request.get_json()
    query = data.get('query')
    top_k = data.get('top_k', 5)  # Default to top 5 results if top_k not specified

    results = process_query(query, top_k)
    print(results)
    return jsonify(results)"""

    # Get JSON data from the request
    data = request.get_json()

    # Validate the query
    is_valid, message = validate_query(data)

    if is_valid:
        # Process the valid query further
        query = data.get('query')
        top_k = data.get('top_k', 5)  # Default to top 5 results if top_k not specified

        # Placeholder for actual query processing logic
        results = process_query(query, top_k)
        print(results)
        return jsonify(results)
    else:
        # Return error message for invalid query
        return jsonify({"error": message}), 400

if __name__ == '__main__':
    app.run(debug=True)
