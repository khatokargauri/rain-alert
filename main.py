import requests
import os
from twilio.rest import Client
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("OWM_API_KEY")
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")
weather_params = {
    "lat" : 19.075983,
    "lon" : 72.877655,
    "appid" : api_key,
    "cnt" : 4
}
response = requests.get(OWM_Endpoint, params = weather_params)
response.raise_for_status()
weather_data = response.json()
#print(weather_data["list"][0]["weather"][0]["id"])
will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True
if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        #messaging_service_sid='MG87f3b73a7762f2a18defff10c03c1f25',
        body="Its going to rain today. Remember to bring an umbrella.",
        from_ = os.environ.get("TWILIO_VIRTUAL_NUMBER "),
        to = os.environ.get("TWILIO_VERIFIED_NUMBER")
    )
    print(message.status)
