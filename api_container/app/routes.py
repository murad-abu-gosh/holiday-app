from datetime import datetime

from flask import Blueprint, render_template, request, jsonify

from app.models.holiday import Holiday
from app.services.holiday_service import HolidayService

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

        if month:
            month = int(month)

        if not country:
            return jsonify({'error': 'Country code is required'}), 400

        holidays = HolidayService.get_holidays(country, month)

        return jsonify([{
            'name': h.name,
            'date': h.date.isoformat(),  # Use iso format() for date serialization
            'type': h.type,
            'greetings': h.greetings
        } for h in holidays])

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@main.route('/add-holiday', methods=['POST'])
def add_holiday():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['name', 'date', 'country', 'type']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        # Create Holiday object
        holiday = Holiday(
            name=data['name'],
            date=datetime.fromisoformat(data['date']).date(),
            country=data['country'].upper(),
            type=data['type'],
            month=datetime.fromisoformat(data['date']).month,
            greetings=data.get('greetings', {})
        )

        # Add holiday to database
        HolidayService.add_holiday(holiday)

        return jsonify({'message': 'Holiday added successfully'})

    except Exception as e:
        print(f"Error adding holiday: {str(e)}")
        return jsonify({'error': str(e)}), 500
