from flask import Flask, jsonify, request
from flask_cors import CORS
import utils

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load data once at startup
print("Initializing backend...")
PI_DIGITS = utils.load_pi_digits()
# Cache results that don't change
DIGIT_DISTRIBUTION_DATA = utils.digit_distribution(PI_DIGITS)
RANDOMNESS_STATS_DATA = utils.randomness_stats(PI_DIGITS)
print("Backend initialized and ready.")

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    if not data or 'sequence' not in data:
        return jsonify({"error": "'sequence' not provided"}), 400

    sequence = data['sequence']
    if not sequence.isdigit() or not sequence:
        return jsonify({"error": "Invalid sequence provided"}), 400
    
    if len(sequence) > 50:
        return jsonify({"error": "Sequence is too long (max 50 digits)"}), 400

    positions = utils.search_all_occurrences(sequence, PI_DIGITS)
    count = len(positions)

    if count > 0:
        first_pos = positions[0]
        snippet = utils.get_snippet(PI_DIGITS, first_pos, sequence)
        response = {
            "found": True,
            "occurrences": count,
            "first_position": first_pos,
            "snippet": snippet
        }
    else:
        response = {"found": False}
    
    return jsonify(response)

@app.route('/digit-distribution', methods=['GET'])
def get_digit_distribution():
    return jsonify(DIGIT_DISTRIBUTION_DATA)

@app.route('/randomness-stats', methods=['GET'])
def get_randomness_stats():
    return jsonify(RANDOMNESS_STATS_DATA)

if __name__ == '__main__':
    # Use a production-ready server like Gunicorn or Waitress in a real deployment
    app.run(port=5000, debug=True)
