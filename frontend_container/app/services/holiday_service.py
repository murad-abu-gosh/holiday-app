from datetime import datetime
from typing import List, Optional

import requests

from app.config import Config
from app.models.holiday import Holiday
from app.repository.holiday_repository import HolidayRepository


class HolidayService:
    @staticmethod
    def get_holidays(country: str, month: Optional[int] = None) -> List[Holiday]:
        # First, try to get holidays from database
        holidays = HolidayRepository.get_holidays(country, month)

        # If no holidays found in database, fetch from API
        if not holidays:
            print(f"No holidays found in database for {country}, fetching from API")
            holidays = HolidayService._fetch_holidays_from_api(country)
            HolidayRepository.save_holidays(holidays)

            # Filter by month if specified
            if month:
                holidays = [h for h in holidays if h.month == month]

        return holidays

    @staticmethod
    def add_holiday(holiday: Holiday) -> None:
        # Add single holiday to database
        print(f"Adding new holiday: {holiday.name} for {holiday.country} with date {holiday.date} and greetings {holiday.greetings}")
        HolidayRepository.add_holiday(holiday)

    @staticmethod
    def _fetch_holidays_from_api(country: str) -> List[Holiday]:
        params = {
            'api_key': Config.HOLIDAY_API_KEY,
            'country': country,
            'year': datetime.now().year
        }

        print(f"Fetching holidays from API for {country}")
        response = requests.get(Config.HOLIDAY_API_URL, params=params)
        response.raise_for_status()

        return [Holiday.from_api_response(item, country)
                for item in response.json()]
