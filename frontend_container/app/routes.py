from datetime import datetime

from flask import Blueprint, render_template, request, jsonify

from app.models.holiday import Holiday
from app.services.holiday_service import HolidayService
from app.config import Config
import requests


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/add')
def add_holiday_page():
    return render_template('add_holiday.html')


@main.route('/holidays', methods=['POST'])
def get_holidays():
    try:
        data = request.get_json()
        country = data.get('country', '').upper()
        month = data.get('month')

        if not country:
            return jsonify({'error': 'Country code is required'}), 400

        # Send request to database handler
        response = requests.get(
            f"{Config.DATABASE_HANDLER_URL}/api/holidays",
            params={"country": country, "month": month}
        )

        return jsonify(response.json()), response.status_code

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@main.route('/add-holiday', methods=['POST'])
def add_holiday():
    try:
        data = request.get_json()

        # Forward the request to the database handler
        response = requests.post(
            f"{Config.DATABASE_HANDLER_URL}/api/holidays",
            json=data
        )

        return jsonify(response.json()), response.status_code

    except Exception as e:
        print(f"Error adding holiday: {str(e)}")
        return jsonify({'error': str(e)}), 500
