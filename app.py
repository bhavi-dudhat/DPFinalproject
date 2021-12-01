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



client = MongoClient("mongodb+srv://Bhavi:dudhat@cluster0.6he2a.mongodb.net/dp?retryWrites=true&w=majority")
db = client['dpProject']
collection = db['weatherData']


app = Flask(__name__)


@app.route('/')
def index():
    client_ip = request.headers.getlist("X-Forwarded-For")[0]
    print(client_ip)
    g = geocoder.ip(client_ip)
    print(g.latlng)
    
    g_time = geocoder.google(g.latlng, method='timezone')    
    x = datetime.now(pytz.timezone(g_time.timeZoneId))
    time = x.strftime("%I")+":"+ x.strftime("%M")+" " +x.strftime("%p")    
    
    url = "https://fcc-weather-api.glitch.me/api/current?lat=%s&lon=%s" % (g.latlng[0], g.latlng[1])
    response = requests.get(url, timeout=(5.05, 27))
    if response.status_code == 200:
        data = json.loads(response.text)
        collection.insert_one(data)
        
        sunrise = datetime.fromtimestamp(int(data['sys']['sunrise']))
        sunset = datetime.fromtimestamp(int(data['sys']['sunset']))
        sunset = f"{sunset:%I:%M %p}"
        sunrise = f"{sunrise:%I:%M %p}"
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
