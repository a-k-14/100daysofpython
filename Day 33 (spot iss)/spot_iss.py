import requests
import datetime
import smtplib
from email.message import EmailMessage
# to run code every 60 seconds
import time

# GOAL
# to know if the iss is passing through current user location within +/- 5 deg lat and long
# if yes, and if the time is night
# then send a mail to the user to look up

# user current location for checking day/night
MY_LAT = 12.968999
MY_LNG = 77.700568
TIME_ZONE = "Asia/Kolkata"
SENDER = "vgstcof@gmail.com"
PASSWORD = "fszk cmil iwwt quby"

# to get iss location
def get_iss_location():
    response = requests.get(url="http://api.open-notify.org/iss-now.json#")
    response.raise_for_status()
    data = response.json()
    # data format
    # {'message': 'success', 'iss_position': {'longitude': '-8.2014', 'latitude': '-36.3030'}, 'timestamp': 1745336383}
    # print(data)
    iss_position = {
        "lat": float(data["iss_position"]["latitude"]),
        "lng": float(data["iss_position"]["longitude"])
    }
    # print(iss_position)

    return iss_position

# return true if the iss lat & lng are within +/- 5 deg of user location lat and lang
def in_proximity():
    iss_position = get_iss_location()
    iss_lat = iss_position["lat"]
    iss_lng = iss_position["lng"]

    print(iss_position)

    return (MY_LAT - 5 <= iss_lat <= MY_LAT + 5) and (MY_LNG - 5 <= iss_lng <= MY_LNG + 5)


# check if the timing at the user location is night, and return True/False
def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0,
        "tzid": TIME_ZONE
    }
    # get the sunrise and sunset timing of the user location
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    # print(response.url)
    data = response.json()
    # data format -> {'results': {'sunrise': '2025-04-22T00:31:33+00:00', 'sunset': '2025-04-22T13:03:50+00:00', ...
    sunrise_time = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset_time = int(data["results"]["sunset"].split("T")[1].split(":", 1)[0])

    now = datetime.datetime.now()
    now_hour = now.hour

    print(sunrise_time, sunset_time, now_hour)

    return now_hour < sunrise_time or now_hour > sunset_time

# send mail alert to the user
def send_mail():
    message = EmailMessage()
    message["From"] = SENDER
    message["To"] = SENDER
    message["Subject"] = "Time to look up for the ISS"
    message.set_content("The ISS will pass by your location!")

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=SENDER, password=PASSWORD)
        connection.send_message(message)

# send mail if iss is in_proximity() and it is_night(), and check this every 60 secs
while True:
    if in_proximity() and is_night():
        print("Sending Mail.........")
        send_mail()
        print("Sent.....")

    time.sleep(60)