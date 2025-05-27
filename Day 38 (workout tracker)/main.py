# GOAL
# build a workout tracker app that stores data on gsheet

import requests
import datetime as dt
import pytz
import os

# Nutritionix API access details
# APP_ID = "02d51993"
# API_KEY = "632d20878daf57bbc68e1286f88a4e0a"
# SHEETY_ENDPOINT = "https://api.sheety.co/ea02cd191d3ecb59125868bb40d3367e/myWorkouts/workouts"
# SHEETY_UN = "suyfv12"
# SHEETY_PW = "djhgb7843!rjehf&dWQ"
# SHEETY_TOKEN = "c3V5ZnYxMjpkamhnYjc4NDMhcmplaGYmZFdR"

APP_ID = os.environ["APP_ID"]
print(APP_ID)
API_KEY = os.environ["API_KEY"]
print(API_KEY)
SHEETY_ENDPOINT = os.environ["SHEETY_ENDPOINT"]
print(SHEETY_ENDPOINT)
SHEETY_UN = os.environ["SHEETY_UN"]
print(SHEETY_UN)
SHEETY_PW = os.environ["SHEETY_PW"]
print(SHEETY_PW)
SHEETY_TOKEN = os.environ["SHEETY_TOKEN"]   
print(SHEETY_TOKEN)



SHEETY_HEADER = {
    "Authorization": f"Basic {SHEETY_TOKEN}"
}

URL = "https://trackapi.nutritionix.com"
ENDPOINT = "/v2/natural/exercise"

HEADERS = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

body = {
    "query": input("Please enter the exercise you've done today: "),
    "weight_kg": 62,
    "height_cm": 164,
    "age": 33,
}

response = requests.post(url=f"{URL}{ENDPOINT}", headers=HEADERS, json=body)
response.raise_for_status()
data = response.json()["exercises"]
workout_data = []

for item in data:
    workout_fragment = {
        "exercise": item["name"].title(),
        "duration": item["duration_min"],
        "calories": item["nf_calories"],
    }
    workout_data.append(workout_fragment)

# print(response.url)
print(response.status_code)

if response.status_code != 200:
    print(response.text)

print(data)

def get_now():
    return dt.datetime.now(tz=pytz.timezone("Asia/Kolkata"))
#


log_date = f"{get_now().date().strftime('%d/%m/%y')}"
log_time = f"{get_now().time().strftime('%I:%M %p')}"

for item in workout_data:
    sheety_payload = {
        "workout":
            {
                "date": log_date,
                "time": log_time,
                "exercise": item["exercise"],
                "duration": item["duration"],
                "calories": item["calories"],
            }
    }
    # sheety_response = requests.post(url=SHEETY_ENDPOINT, headers=SHEETY_HEADER, json=sheety_payload)
    sheety_response = requests.post(url=SHEETY_ENDPOINT, auth=(SHEETY_UN, SHEETY_PW), json=sheety_payload)
    sheety_response.raise_for_status()
    print(sheety_response.status_code)
    print(sheety_response.text)
    # print(sheety_response.json())

