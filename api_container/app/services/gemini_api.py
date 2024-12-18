"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import google.generativeai as genai
from app.config import Config



genai.configure(api_key=Config.GEMINI_API_KEY)

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings

    system_instruction='''Generate JSONs of Holidays, based on the country code given.
The JSON will be in the following format:
-name: The name of the holiday.

-date: The date of the holiday in the format YYYY-MM-DD.

-country: The two-letter country code or region where the holiday is celebrated.

-type: The type of holiday. One of the following: National, Religious, Cultural, Observance, Other.

-month: The month number of the holiday.

-greetings: An object containing greeting messages in various languages, with language codes as keys (en, ar, he, ru, fr).

Here are examples of JSONs:

[
  {
    "name": "Christmas Day",
    "date": "2023-12-25",
    "country": "US",
    "type": "Religious",
    "month": 12,
    "greetings": {
      "en": "Merry Christmas!",
      "ar": "عيد ميلاد مجيد",
      "he": "חג מולד שמח",
      "ru": "С Рождеством!",
      "fr": "Joyeux Noël!"
    }
  },
  {
    "name": "Hanukkah",
    "date": "2023-12-18", // Approximate start date
    "country": "IL",
    "type": "Religious",
    "month": 12,
    "greetings": {
      "en": "Happy Hanukkah!",
      "ar": "حانوكا سعيد",
      "he": "חנוכה שמח",
      "ru": "С Ханукой!",
      "fr": "Joyeux Hanoukka!"
    }
  },
  {
    "name": "Eid al-Fitr",
    "date": "2024-03-22", // Approximate start date
    "country": "SA",
    "type": "Religious",
    "month": 3,
    "greetings": {
      "en": "Eid Mubarak!",
      "ar": "عيد مبارك",
      "he": "עיד אל-פיטר שמח",
      "ru": "С праздником Ид аль-Фитр!",
      "fr": "Joyeuse Aid el-Fitr!"
    }
  },
  {
    "name": "Chinese New Year",
    "date": "2024-02-10",
    "country": "CN",
    "type": "Cultural",
    "month": 2,
    "greetings": {
      "en": "Happy Chinese New Year!",
      "ar": "سنة جديدة صينية سعيدة",
      "he": "שנה סינית חדשה שמח",
      "ru": "С Новым годом по китайскому календарю!",
      "fr": "Bonne année chinoise!"
    }
  },
  {
    "name": "Diwali",
    "date": "2023-11-12", // Approximate start date
    "country": "IN",
    "type": "Religious",
    "month": 11,
    "greetings": {
      "en": "Happy Diwali!",
      "ar": "ديوالي سعيد",
      "he": "דיוואלי שמח",
      "ru": "Счастливой Дивали!",
      "fr": "Joyeux Diwali!"
    }
  },
  {
    "name": "Thanksgiving Day",
    "date": "2023-11-23",
    "country": "US",
    "type": "Cultural",
    "month": 11,
    "greetings": {
      "en": "Happy Thanksgiving!",
      "ar": "عيد الشكر السعيد",
      "he": "יום ההודיה שמח",
      "ru": "С Днем благодарения!",
      "fr": "Joyeux Thanksgiving!"
    }
  },
  {
    "name": "Independence Day", 
    "date": "2023-07-04",
    "country": "US",
    "type": "National",
    "month": 7,
    "greetings": {
      "en": "Happy 4th of July!",
      "ar": "عيد الاستقلال الأمريكي سعيد",
      "he": "יום העצמאות האמריקאי שמח",
      "ru": "С Днем независимости США!",
      "fr": "Joyeux 4 juillet!"
    }
  },
  {
    "name": "Bastille Day",
    "date": "2023-07-14",
    "country": "FR",
    "type": "National",
    "month": 7,
    "greetings": {
      "en": "Happy Bastille Day!",
      "ar": "عيد الباستيل سعيد",
      "he": "יום הבסטיליה שמח",
      "ru": "С Днем взятия Бастилии!",
      "fr": "Joyeuse fête nationale!"
    }
  },
  {
    "name": "Halloween",
    "date": "2023-10-31",
    "country": "US",
    "type": "Cultural",
    "month": 10,
    "greetings": {
      "en": "Happy Halloween!",
      "ar": "عيد الهالوين سعيد",
      "he": "חגיגת ליל כל הקדושים שמח",
      "ru": "С Хэллоуином!",
      "fr": "Joyeux Halloween!"
    }
  },
  {
    "name": "Ramadan",
    "date": "2024-03-10", // Approximate start date
    "country": "SA",
    "type": "Religious",
    "month": 3,
    "greetings": {
      "en": "Ramadan Kareem!",
      "ar": "رمضان كريم",
      "he": "רמדאן קרים",
      "ru": "Рамадан Карим!",
      "fr": "Ramadan Kareem!"
    }
  }
]


Generate only JSONs. Only respond with the list of JSONs. Do NOT respond with something like "Here are 10 JSONs...".
Try generating holidays from all nationalities/cultures/religions that live in that country. Be inclusive.
Try making the greetings more specific to that holiday, instead of using the word 'happy' in the greeting. For example, use 'Ramadan Kareem' instead of 'Happy Ramadan'.
Generate the holidays randomly.'''
)

chat_session = model.start_chat(
)

import json
import re


def extract_and_convert_to_json(json_string):
    """
    Extracts the JSON list from a string and converts it into a list of dictionaries.

    Parameters:
    json_string (str): String containing the JSON list.

    Returns:
    list: A list of dictionaries.
    """
    try:
        # Use regex to find the list brackets and extract the content within
        match = re.search(r'\[.*]', json_string, re.DOTALL)
        if match:
            json_list_string = match.group(0)
            dict_list = json.loads(json_list_string)
            return dict_list
        else:
            print("No JSON list found in the provided string.")
            return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []


def generate_10_greetings_list(country: str):
    response = chat_session.send_message(f"Generate 5 holidays for {country}")
    print(f'gemini response text: {response.text}')
    greetings_list = extract_and_convert_to_json(response.text)
    print(f'greetings to JSON: {greetings_list}')
    return greetings_list


if __name__ == '__main__':
    sent = generate_10_greetings_list('IL')
    print(sent)
