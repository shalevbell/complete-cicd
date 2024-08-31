from flask import Flask, render_template, request
import json
from datetime import date
from os import listdir, environ
from os.path import isfile, join
from logic import *

weather_app = Flask(__name__)  # create a new application instance called weather_app.

BG_COLOR = environ.get('BG_COLOR', '#e6dabc') # Set bg as env variable BG_COLOR


@weather_app.route('/', methods=('GET', 'POST'))  # Sets an app rout and gives it GET & POST methods.
def search():
    if request.method == 'POST':
        button = request.form.get('submit_button')
        
        if button == 'history':
            # Retrieve list of history files
            history_files = [
                f for f in listdir('static/history/')
                if isfile(join('static/history/', f))
            ]
            return render_template('weather_history.html', history=history_files, bg=BG_COLOR)
        
        elif button == 'check':
            location = request.form.get('input_location')
            try:
                # Convert location to dictionary and save to file
                location_dict = location_to_dict(location)
                file_path = f'static/history/{location}:{date.today()}.json'
                with open(file_path, 'w') as outfile:
                    json.dump(location_dict, outfile, indent=4)
                
                return render_template('weather_main.html', location_dict=location_dict, bg=BG_COLOR)
            except TypeError:
                # Handle invalid location
                return render_template('weather_error.html', bg=BG_COLOR)

    return render_template('weather_search.html', bg=BG_COLOR)


if __name__ == "__main__":
    weather_app.run(host='0.0.0.0')  # Runs weather_app.
