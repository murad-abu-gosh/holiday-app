from typing import List, Optional

from app.models.holiday import Holiday
from app.repository.init_db import db


class HolidayRepository:
    COLLECTION = 'holidays'

    @staticmethod
    def get_holidays(country: str, month: Optional[int] = None) -> List[Holiday]:
        query = {'country': country}
        if month:
            query['month'] = month

        print(f"Searching holidays with query: {query}")
        holidays_data = db.find(HolidayRepository.COLLECTION, query)
        print(f"Found {len(holidays_data)} holidays")
        # print all holidays data
        for h in holidays_data:
            print(h)

        return [Holiday.from_dict(h) for h in holidays_data]

    @staticmethod
    def save_holidays(holidays: List[Holiday]) -> None:
        if not holidays:
            return

        holidays_data = [h.to_dict() for h in holidays]
        db.insert_many(HolidayRepository.COLLECTION, holidays_data)

    @staticmethod
    def add_holiday(holiday: Holiday) -> None:
        holiday_data = holiday.to_dict()
        print(f"Adding holiday in function add_holiday: {holiday_data}")
        db.insert_many(HolidayRepository.COLLECTION, [holiday_data])
