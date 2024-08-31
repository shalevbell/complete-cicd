import requests  # used to request api from the web
from datetime import datetime  # Used to check today's day


def location_to_api(user_input):
    """
    Return the url api with the location the user inputted
    :param user_input: Is the location the user inputted.
    :return: The api url.
    """
    api = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{user_input}?" \
          f"unitGroup=metric&include=days%2Ccurrent%2Chours&key=[your_key_here]&contentType=json"
    return api


def api_to_dict(api_data):
    """
    Return a dictionary with relevant info from api
    :param api_data: Is the api url.
    :return: A dictionary with all relevant data from the api.
    """
    today = datetime.today().strftime('%A')  # today's date.
    d1 = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", ]
    i = d1.index(today)  # the index of today's date.
    days = d1[i:]  # select all days from before today.
    days.extend((d1[:i]))  # append all the days to the end of the list.

    try:  # Tries to access the data as a json, if not a valid location raises an error.
        data_dict = {
            "c_location": api_data.json()["resolvedAddress"],
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
    api1 = location_to_api(location)
    return api_to_dict(requests.get(api1))
