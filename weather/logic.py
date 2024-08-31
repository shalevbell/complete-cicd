import requests  # used to request api from the web
from datetime import datetime  # Used to check today's day
import os

def location_to_api(user_input):
    """
    Constructs the API URL for the given location.

    :param user_input: Location provided by the user.
    :return: The API URL as a string.
    """
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise EnvironmentError("API_KEY environment variable is not set")
    
    api_url = (
        f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{user_input}?"
        f"unitGroup=metric&include=days%2Ccurrent%2Chours&key={api_key}&contentType=json"
    )
    return api_url


def api_to_dict(api_data: requests.Response):
    """
    Parses the API response and extracts relevant weather information.

    :param api_response: The response object from the API request.
    :return: A dictionary with relevant weather data.
    :raises ValueError: If the API response is invalid.
    """
    try:
        data = api_data.json()
    except ValueError:
        raise ValueError("Invalid JSON response from API")
    
    today = datetime.today().strftime('%A')  # today's date.
    days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", ]
    i = days.index(today)
    days = days[i:] + days[:i]

    data_dict = {
        "c_location": data["resolvedAddress"],
        "c_temp": data["currentConditions"]["temp"],
        "c_humidity": data["currentConditions"]["humidity"],
        "c_uv": data["currentConditions"]["uvindex"],
        "c_sunrise": data["currentConditions"]["sunrise"],
        "c_sunset": data["currentConditions"]["sunset"],
        "c_description": data["currentConditions"]["conditions"]
    }

    for x in range(7):
        day_data = data["days"][x]
        data_dict[days[x]] = (
            day_data["hours"][11]["temp"], 
            day_data["hours"][23]["temp"]
        )

    return day_data


def location_to_dict(location):
    """
    Return a dict with relevant info by receiving the location name.
    Is a shortcut to make a dict from a location string
    :param location: The location the user inputted.
    :return: A dict with all relevant data from the api.
    """
    api_url = location_to_api(location)
    response = requests.get(api_url)
    response.raise_for_status()

    return api_to_dict(response)
