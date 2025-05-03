import requests
import datetime as dt

parameters = {
    "lat": 12.968999,
    "lng": 77.700568,
    "formatted": 0
}

# get the sunrise and sunset times for a location
response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":", 1)[0])

# print(data)
# print(response.url)
# print(type(int(sunrise)))

now = dt.datetime.now()
hour = now.hour
print(hour)

print(sunrise > hour)