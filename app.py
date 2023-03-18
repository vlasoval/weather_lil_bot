from flask import Flask, request
# from flask_sqlalchemy import SQLAlchemy
import requests

# db = SQLAlchemy()
# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# db.init_app(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     city = db.Column(db.String,  nullable=True)

# with app.app_context():
#     db.create_all() 

@app.route("/", methods=["GET", "POST"])
def receive_update():   
    if request.method == "POST":
        print(request.json)
        chat_id1=request.json['message']['chat']['id']

        try:       
            # user = User(
            #     id=request.json['message']['from']['id'],
            #     city=request.json['message']['text'],
            # )
            # db.session.add(user)
            # db.session.commit()
            city=request.json['message']['text']
            city_coord=get_coord_city(city)
            weather = get_weather(city_coord.lat, city_coord.lon, city)
            currency = get_currency()
            send_message(chat_id1, weather+'\n'+currency)
        except Exception as ex:
            send_message(chat_id1, 'Ошибка(')
            print(ex)
        
    return {"ok": True}


def send_message(chat_id, text):
    method = "sendMessage"
    token = ""
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)

def get_coord_city(city):
    params1={"limit": "1", "appid": "", "q":city}
    api_city_result = requests.get(f'http://api.openweathermap.org/geo/1.0/direct',params1)
    api_city_response = api_city_result.json()
    lat=api_city_response[0]['lat']
    lon=api_city_response[0]['lon']
    return LatLon(lat, lon)
class LatLon():
    def __init__(self, lat, lon):
        self.lat=lat
        self.lon=lon



def get_weather(lat, lon, city):
    params2 = {"appid": "", "lat": lat, "lon": lon, 'units':'metric', 'lang':'ru' }
    api_result = requests.get('https://api.openweathermap.org/data/2.5/weather',params2)
    api_response = api_result.json()
    return f"Сейчас в {city}е {api_response['main']['temp_min']} градусов, {api_response['weather'][0]['description']}"

def get_currency():
    api_result2 = requests.get('https://www.nbrb.by/api/exrates/rates/431')
    api_result3 = requests.get('https://www.nbrb.by/api/exrates/rates/451')
    api_response2 = api_result2.json()
    api_response3 = api_result3.json()
    return f"Курс доллара на сегодня {api_response2['Cur_OfficialRate']}, курс евро {api_response3['Cur_OfficialRate']}"
