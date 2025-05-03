import requests
from twilio.rest import Client

# to make a weather forecast app that sends sms if there is rain in next 12h forecast

# OWM details
OWM_API_KEY = "2ee401733e81ae2b390aa38420e3daa2"
MY_LAT = 9.740528106689453
MY_LON = 118.73297119140625

# twilio details
ACCOUNT_SID = "AC896131eb83cf52f4568c9e7ca5ca8a35"
AUTH_TOKEN = "21326ca5d58e307c182f987d6e394c8f"
MY_PH = "+13185438874"

parameters = {
    "lat": MY_LAT,
    "lon": MY_LON,
    "appid": OWM_API_KEY,
    "units": "metric",
    "cnt": 4
}

response = requests.get(url="http://api.openweathermap.org/data/2.5/forecast", params=parameters)
response.raise_for_status()
data = response.json()
# print(response.url)
# print(data)
print(data["city"]["name"])
forecast_4days = data["list"]

for item in forecast_4days:
    # print(item["dt_txt"])
    # print(item["weather"][0]["main"])
    # if the id (condition code) is < 700 (200 - ts, 300 - drizzle, 500 - Rain, 600 - snow), then we need ☔
    # print(type(item["weather"][0]["id"]))
    if item["weather"][0]["id"] < 700:
        print("Bring Umbrella☔")
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(body=f'''It's going to rain in {data["city"]["name"]}. Bring an umbrella☔.''', to="+917019467824", from_=MY_PH)
        print(message.status)
        break