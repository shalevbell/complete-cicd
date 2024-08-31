from flask import Flask, render_template, request  # needed to use flask.
from app import *  # imports all functions from app.py.
import json
from datetime import date
from os import listdir
from os.path import isfile, join
import os

weather_app = Flask(__name__)  # create a new application instance called weather_app.
bg = os.environ['BG_COLOR'] # Set bg as env variable BG_COLOR


@weather_app.route('/', methods=('GET', 'POST'))  # Sets an app rout and gives it GET & POST methods.
def search():
    if request.method == "POST":  # checks if the user is sending a POST request.
        if request.form['submit_button'] == 'history':  # If user presses history button then execute
            files = [f for f in listdir("static/history/") if isfile(join("static/history/", f))]
            return render_template('weather_history.html', history=files, bg=bg)
        elif request.form['submit_button'] == 'check':  # If user presses search button then execute
            try:  # Checks if location_to_dict raised a typeError because the location was not valid.
                location = request.form["input_location"]
                location_dict = location_to_dict(location)
                with open(f"static/history/{location}:{date.today()}.json", 'w') as outfile:
                    json.dump(location_dict, outfile, indent=4)
            except TypeError:  # send user to Error page.
                return render_template('weather_error.html', bg=bg)

        return render_template('weather_main.html', location_dict=location_dict, bg=bg)

    return render_template('weather_search.html', bg=bg)


if __name__ == "__main__":
    weather_app.run(host='0.0.0.0')  # Runs weather_app.
