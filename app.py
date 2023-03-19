import requests
import os

from flask import Flask, request


class LatLon:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def receive_update():
    if request.method == "POST":
        chat_id = request.json["message"]["chat"]["id"]

        try:
            city = request.json["message"]["text"]
            coordinates = get_coordinates_by_city(city)
            weather = get_weather(coordinates, city)
            currency = get_currency()
            send_message(chat_id, weather + "\n" + currency)
        except Exception as ex:
            send_message(chat_id, "Ошибка(")

    return {"ok": True}


def send_message(chat_id, text):
    token = os.environ["TELERAM_BOT_TOKEN"]
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id, 
        "text": text
    }
    requests.post(url, data=data)


def get_coordinates_by_city(city):
    params1 = {
        "limit": "1", 
        "appid": os.environ["WEATHER_APP_ID"], 
        "q": city
    }
    api_city_result = requests.get(
        f"http://api.openweathermap.org/geo/1.0/direct", params1
    )
    api_city_response = api_city_result.json()
    lat = api_city_response[0]["lat"]
    lon = api_city_response[0]["lon"]
    return LatLon(lat, lon)


def get_weather(coordinates, city):
    params = {
        "appid": os.environ["WEATHER_APP_ID"], 
        "lat": coordinates.lat, 
        "lon": coordinates.lon, 
        "units": "metric", 
        "lang": "ru"
    }
    result = requests.get(
        "https://api.openweathermap.org/data/2.5/weather", params
    ).json()
    return f"Сейчас в {city}е {api_response['main']['temp_min']} градусов, {api_response['weather'][0]['description']}"


def get_currency():
    usd_currency_response = requests.get("https://www.nbrb.by/api/exrates/rates/431")
    eur_curency_response = requests.get("https://www.nbrb.by/api/exrates/rates/451")
    usd_result = usd_currency_response.json()
    eur_result = eur_curency_response.json()
    return f"Курс доллара на сегодня {usd_result['Cur_OfficialRate']}, курс евро {eur_result['Cur_OfficialRate']}"
