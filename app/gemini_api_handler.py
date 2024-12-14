from flask import Flask, jsonify, request
import random
from app.services.gemini_api import generate_10_sentence_objects
app = Flask(__name__)

@app.route('/random_numbers', methods=['GET'])
def random_numbers():
    # Get the 'count' parameter from the request, default to 10 if not provided
    # count = request.args.get('count', default=10, type=int)

    # Generate a list of random numbers
    numbers = generate_10_sentence_objects()

    # Return the list of random numbers as JSON
    return numbers
    # return jsonify({
    #     'count': count,
    #     'numbers': numbers
    # })

if __name__ == '__main__':
    app.run(debug=True)