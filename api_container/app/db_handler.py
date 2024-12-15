import config
from flask import Flask, jsonify, request
from typing import List, Optional
import os

from app.models.holiday import Holiday
from app.services.holiday_service import HolidayService
from app.config import Config

db_app = Flask(__name__)

# Initialize database
from app.repository.database import Database
db = Database(region=Config.AWS_REGION)


@db_app.route('/api/holidays', methods=['GET'])
def get_holidays():
    """
    Get holidays for a specific country and optionally filtered by month.
    Query parameters:
    - country: Two-letter country code (required)
    - month: Month number 1-12 (optional)
    """
    country = request.args.get('country')
    month = request.args.get('month')

    if not country:
        return jsonify({'error': 'Country code is required'}), 400

    try:
        if month:
            month = int(month)
            if not 1 <= month <= 12:
                return jsonify({'error': 'Month must be between 1 and 12'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid month format'}), 400

    try:
        holidays = HolidayService.get_holidays(country, month)
        return jsonify([holiday.to_dict() for holiday in holidays])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@db_app.route('/api/holidays', methods=['POST'])
def add_holiday():
    """
    Add a new holiday.
    Expected JSON body:
    {
        "name": "Holiday Name",
        "date": "2024-12-25",
        "country": "US",
        "type": "National",
        "greetings": {
            "en": "Happy Holiday!",
            "fr": "Joyeuses fêtes!"
        }
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        required_fields = ['name', 'date', 'country', 'type']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

        holiday = Holiday.from_dict(data)
        HolidayService.add_holiday(holiday)
        return jsonify({'message': 'Holiday added successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@db_app.route('/api/holidays/<country>', methods=['GET'])
def get_country_holidays(country):
    """Get all holidays for a specific country"""
    try:
        holidays = HolidayService.get_holidays(country)
        return jsonify([holiday.to_dict() for holiday in holidays])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


