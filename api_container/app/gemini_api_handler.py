from flask import Flask, jsonify, request
import random
from app.services.gemini_api import generate_10_greetings_list
gemini_app = Flask(__name__)

@gemini_app.route('/<country>', methods=['GET'])
def get_country_holidays(country):
    # Get the 'count' parameter from the request, default to 10 if not provided
    # count = request.args.get('count', default=10, type=int)

    # Generate a list of random numbers
    greetings = generate_10_greetings_list(country)

    # Return the list of holiday greetings as JSON
    return jsonify(greetings)


    # return greetings
    # return jsonify({
    #     'count': count,
    #     'numbers': numbers
    # })

