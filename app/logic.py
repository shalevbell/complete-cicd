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
    d = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", ]
    i = d.index(today)  # the index of today's date.
    days = d[i:]  # select all days from before today.
    days.extend((d[:i]))  # append all the days to the end of the list.

    try:  # Tries to access the data as a json, if not a valid location raises an error.
        data_dict = {
            "c_lcation": api_data.json()["resolvedAddress"],
            "c_temp": api_data.json()["currentConditions"]["temp"],
            "c_humidity": api_data.json()["currentConditions"]["humidity"],
            "c_uv": api_data.json()["currentConditions"]["uvindex"],
            "c_sunrise": api_data.json()["currentConditions"]["sunrise"],
            "c_sunset": api_data.json()["currentConditions"]["sunset"],
            "c_description": api_data.json()["currentConditions"]["conditions"]
        }
    except:
        raise TypeError

    for x in range(7):  # Updates dict with temp in day and night for each day of the week.
        data_dict.update({
            days[x]: (api_data.json()["days"][x]["hours"][11]["temp"], api_data.json()["days"][x]["hours"][23]["temp"])
        })
    return data_dict


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
