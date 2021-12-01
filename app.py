import requests
import json
import geocoder
from flask import Flask, render_template
import pprint
import datetime
# from apscheduler.scheduler import Scheduler
from pymongo import MongoClient
import requests as requests


client = MongoClient("mongodb+srv://Bhavi:dudhat@cluster0.6he2a.mongodb.net/dp?retryWrites=true&w=majority")
db = client['dpProject']
collection = db['weatherData']


x = datetime.datetime.now()
time = x.strftime("%I")+":"+ x.strftime("%M")+" " +x.strftime("%p")

app = Flask(__name__)


@app.route('/')
def index():
    g = geocoder.ip('me')
    print(g.latlng)
    
    ip = requests.get('https://ip.seeip.org').text
    print(ip)

    url = "https://fcc-weather-api.glitch.me/api/current?lat=%s&lon=%s" % (g.latlng[0], g.latlng[1])
    response = requests.get(url, timeout=(5.05, 27))
    if response.status_code == 200:
        data = json.loads(response.text)
        collection.insert_one(data)
        
        sunrise = datetime.datetime.fromtimestamp(int(data['sys']['sunrise']))
        sunset = datetime.datetime.fromtimestamp(int(data['sys']['sunset']))
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
