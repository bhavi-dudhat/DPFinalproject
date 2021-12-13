import requests
import json
import geocoder
from flask import Flask, render_template
import pprint
from datetime import datetime, timezone
from pymongo import MongoClient
import requests as requests
from flask import request
import time
from time import strftime, localtime

client = MongoClient("mongodb+srv://Bhavi:dudhat@cluster0.6he2a.mongodb.net/dp?retryWrites=true&w=majority")
db = client['dpProject']
collection = db['weatherData']

time = strftime('%B %d, %Y', localtime())

app = Flask(__name__)

@app.route('/')
def index():
    client_ip = request.headers.getlist("X-Forwarded-For")[0]
    print(client_ip)
    g = geocoder.ip(client_ip)
    print(g.latlng)
    
    url = "https://fcc-weather-api.glitch.me/api/current?lat=%s&lon=%s" % (g.latlng[0], g.latlng[1])
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        collection.insert_one(data)
        sunrise = strftime('%I:%M %p', localtime(int(data['sys']['sunrise'])))
        sunset = strftime('%I:%M %p', localtime(int(data['sys']['sunset'])))
        for i in data['weather'] :
            weather = i['main']
        visibility = data['visibility']/1000
        pressure = data['main']['pressure']
        print(visibility)
        pprint.pprint(data)
        return render_template('index.html',data=data, time=time, sunrise=sunrise, sunset=sunset, visibility = visibility, weather = weather, pressure=pressure)

if __name__ == '__main__':
    app.run(debug=True)
    app.enable('trust proxy')
