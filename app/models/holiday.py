from datetime import datetime, date
from typing import Optional, Dict


class Holiday:
    """
    Represents a holiday with multilingual greetings.

    Attributes:
        name (str): The name of the holiday
        date (date): The date of the holiday
        country (str): Two-letter country code
        type (str): Type of holiday (National, Religious, etc.)
        month (int): Month of the holiday
        greetings (Dict[str, str]): Dictionary of greetings in different languages
    """

    # Language codes and their display names
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'ar': 'Arabic',
        'he': 'Hebrew',
        'ru': 'Russian',
        'fr': 'French'
    }

    def __init__(self, name: str, date: date, country: str, type: str,
                 greetings: Optional[Dict[str, str]] = None, month: Optional[int] = None):
        self.name = name
        self.date = date
        self.country = country
        self.type = type
        self.greetings = greetings or {}
        self.month = month if month else date.month

    @staticmethod
    def from_api_response(response: dict, country: str) -> 'Holiday':
        """Creates a Holiday instance from API response data."""
        date_obj = datetime.strptime(response['date'], '%Y-%m-%d').date()
        return Holiday(
            name=response['name'],
            date=date_obj,
            country=country,
            type=response.get('type', 'National'),
            greetings={}
        )

    def to_dict(self) -> dict:
        """Converts the Holiday instance to a dictionary for database storage."""
        return {
            'name': self.name,
            'date': self.date.isoformat(),
            'country': self.country,
            'type': self.type,
            'month': self.month,
            'greetings': self.greetings
        }

    @staticmethod
    def from_dict(data: dict) -> 'Holiday':
        """Creates a Holiday instance from a dictionary retrieved from the database."""
        return Holiday(
            name=data['name'],
            date=datetime.fromisoformat(data['date']).date(),
            country=data['country'],
            type=data['type'],
            greetings=data.get('greetings', {}),
            month=data.get('month')
        )
