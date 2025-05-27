# GOAL
# to collect user details (name and email id)
# check if there are flights lower than set price for destinations in gsheet
# if yes, send email alerts to the users

import requests
import os
import pandas as pd
import json
import time

from soupsieve.util import lower

from alerts import send_alerts

start_time = time.time()

# get the list of users and destinations list from gsheet via sheety
SHEETY_TOKEN = os.environ.get("SHEETY_TOKEN")
AMADEUS_API_KEY = os.environ.get("AMADEUS_API_KEY")
AMADEUS_API_SECRET = os.environ.get("AMADEUS_API_SECRET")
# conversion rate to INR, presently EUR -> INT
EXCHANGE_RATE = 96.21


# get the list of destinations from gsheet
def get_destinations() -> list:
    sheety_url = "https://api.sheety.co/ea02cd191d3ecb59125868bb40d3367e/flightDeals/prices"
    sheety_auth_header = {
        "Authorization": f"Bearer {SHEETY_TOKEN}"
    }

    # csv file to store destinations to avoid calling sheety api on every run
    data_file = "destinations.csv"
    # to enforce refresh via sheety api
    refresh_destinations = False


    # if the file exists and if the file is not empty and forced refresh is False
    if os.path.exists(data_file) and os.path.getsize(data_file) > 0 and not refresh_destinations:
        print(time.strftime("%d-%b-%Y %I:%M:%S %p"), "-> Getting destinations data from", data_file)
        # missing values have nan, to avoid nan we fill them with "" empty string
        df = pd.read_csv(data_file).fillna("")
        destinations_list = df.to_dict(orient="records")
        # print(destinations_list)
        return destinations_list
    else:
        # if the file does not exist, or it is empty or forced refresh is True
        print(time.strftime("%d-%b-%Y %I:%M:%S %p"), "-> Getting destinations data from gsheet via sheety")
        response = requests.get(url=sheety_url, headers=sheety_auth_header)
        response.raise_for_status()

        if response.status_code != 200:
            print(response.text)
            return []
        else:
            destinations_list = response.json()["prices"]

            # update iata code
            for item in destinations_list:
                if item["iataCode"] == "":
                    item["iataCode"] = get_iatacode(item["city"])

                # add iata code to gsheet
                payload = {
                    "price" : {
                        "iataCode": item["iataCode"]
                    }
                }

                put_response = requests.put(url=f"{sheety_url}/{item['id']}", json=payload, headers=sheety_auth_header)
                put_response.raise_for_status()

            pd.DataFrame(destinations_list).to_csv(data_file, index=False)
            # print(destinations_list)
            return destinations_list


# get the list of users from gsheet
def get_users() -> list:
    sheety_url = "https://api.sheety.co/ea02cd191d3ecb59125868bb40d3367e/flightDeals/users"
    sheety_auth_header = {
        "Authorization": f"Bearer {SHEETY_TOKEN}"
    }

    data_file = "users.csv"
    refresh_data = False

    if os.path.exists(data_file) and os.path.getsize(data_file) and not refresh_data:
        print(time.strftime("%d-%b-%Y %I:%M:%S %p"), "-> Getting users data from", data_file)
        df = pd.read_csv(data_file)
        users_list = df.to_dict(orient="records")
        # print(users_list)
        return users_list
    else:
        print(time.strftime("%d-%b-%Y %I:%M:%S %p"), "-> Getting users data from gsheet via sheety")
        response = requests.get(url=sheety_url, headers=sheety_auth_header)
        response.raise_for_status()

        if response.status_code != 200:
            print(response.text)
            return []
        else:
            users_list = response.json()["users"]
            pd.DataFrame(users_list).to_csv(data_file, index=False)
            print(users_list)
            return users_list


def get_amadeus_token() -> str:

    data_file = "token.json"
    refresh_token = False
    # to prevent unbounded growth of token.json over time
    max_tokens = 10

    data = {
        "grant_type": "client_credentials",
        "client_id": AMADEUS_API_KEY,
        "client_secret": AMADEUS_API_SECRET,
    }

    header = {
        "content-type": "application/x-www-form-urlencoded",
    }

    url = "https://test.api.amadeus.com/v1/security/oauth2/token"

    if os.path.exists(data_file) and os.path.getsize(data_file) and not refresh_token:
        print(time.strftime("%d-%b-%Y %I:%M:%S %p"), "-> Getting token from", data_file)
        with open(data_file) as f:
            token_list = json.load(f)
            latest_token = token_list[-1]

        # return the locally stored token if it is not expired
        if latest_token["expires_at"] > time.time():
            return latest_token["access_token"]

    print(time.strftime("%d-%b-%Y %I:%M:%S %p"), "-> Getting new token from amadeus")
    response = requests.post(url, data=data, headers=header)
    response.raise_for_status()
    data = response.json()
    access_token = data["access_token"]
    expires_in = data["expires_in"]
    state = data.get("state", "NA")

    new_token = {
        "access_token": access_token,
        "expires_at": expires_in + time.time(),
        "state": state,
        "timestamp": time.strftime("%d-%b-%Y %I:%M:%S %p")
    }

    # check file exists + not empty data or file exists + empty data or file does not exist
    try:
        with open(data_file) as f:
            token_list = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        token_list = []

    token_list.append(new_token)
    # limit the number of tokens stored in the JSON
    token_list = token_list[-max_tokens:]
    with open(data_file, mode="w") as f:
        json.dump(token_list, f, indent=2)

    return access_token


def get_iatacode(city) -> str:
    print(time.strftime("%d-%b-%Y %I:%M:%S %p"), "-> Getting IATA code for", city)
    city = city if len(city) <= 10 else city[:9]
    url = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
    params = {
        "keyword": city,
    }
    header = {
        "Authorization": f"Bearer {get_amadeus_token()}"
    }

    response = requests.get(url, params=params, headers=header)
    response.raise_for_status()

    # check for count > 0 to catch cases where there is no iata code for a city
    if response.status_code == 200 and response.json()["meta"]["count"] > 0:
        data = response.json()
        # print(data)
        iatacode = data["data"][0]["iataCode"]
    else:
        print(response.status_code)
        print(response.text)
        iatacode = ""
    # print(iatacode)
    return iatacode


# get the latest and lowest price for origin and destination along with other data from "Flight Offers Search" API
# for direct and layover flights
def get_current_offer(origin_iatacode, destination_iatacode, departure_date) -> dict:
    # print(time.strftime("%d-%b-%Y %I:%M:%S %p"), "-> Getting current offer for", origin_iatacode, "to", destination_iatacode, "on", departure_date)
    url = "https://test.api.amadeus.com/v2"
    endpoint = "/shopping/flight-offers"

    header = {
        "Authorization": f"Bearer {get_amadeus_token()}"
    }

    # departure date - 2023-05-02
    params = {
        "originLocationCode": origin_iatacode,
        "destinationLocationCode": destination_iatacode,
        "departureDate": departure_date,
        "adults": 1,
        "nonStop": "true",
        "max": 1,
    }

    # direct flights
    direct_response = requests.get(url=f"{url}{endpoint}", headers=header, params=params)
    direct_response.raise_for_status()
    direct_data = direct_response.json()["data"]

    # layover flights
    params["nonStop"] = "false"
    layover_response = requests.get(url=f"{url}{endpoint}", headers=header, params=params)
    layover_response.raise_for_status()
    layover_data = layover_response.json()["data"]

    # compare prices of direct vs. layover flights
    # mode - direct vs. layover
    # best_data - direct vs. layover WIL in price
    if len(direct_data) != 0:
        direct_price = float(direct_data[0]["price"]["total"])
        layover_price = float(layover_data[0]["price"]["total"])
        best_data = layover_data if layover_price < direct_price else direct_data
        mode = "layover" if layover_price < direct_price else "direct"
    else:
        best_data = layover_data
        mode = "layover"

    data = best_data[0]
    # print(data)
    segments = data["itineraries"][0]["segments"]
    route: list = [origin_iatacode]
    for segment in segments:
        route.append(segment["arrival"]["iataCode"])

    departure_date_time = data["itineraries"][0]["segments"][0]["departure"]["at"].split("T")

    # data to return
    offer_data = {
    "origin_iatacode": origin_iatacode,
    "destination_iatacode": destination_iatacode,
    "journey_date": departure_date_time[0],
    "journey_time": departure_date_time[1],
    "currency": data["price"]["currency"],
    "price": data["price"]["total"],
    "price_inr": float(data["price"]["total"]) * EXCHANGE_RATE,
    "seats_available": data["numberOfBookableSeats"],
    "route": " -> ".join(route),
    "mode": mode,
    }

    # print(offer_data)
    return offer_data


# get the destinations which have deals i.e., the current ticket price <= set price in gsheet
def get_destinations_with_deals(destinations_list, from_iatacode, departure_date) -> list:
    print(time.strftime("%d-%b-%Y %I:%M:%S %p"), "-> Getting destinations with deals...")
    destinations_with_deals_list: list = []

    for item in destinations_list:
        # print(item.get("iataCode"))
        if item.get("iataCode"):
            offer = get_current_offer(origin_iatacode=from_iatacode,
                                      destination_iatacode=item["iataCode"],
                                      departure_date=departure_date,
                                      )
            if float(offer["price"]) <= float(item["lowestPrice"]):
                offer["origin_city"] = origin_city
                offer["destination_city"] = item["city"]
                destinations_with_deals_list.append(offer)
        else:
            print(f"IATA code not available for {item['city']}")

    return destinations_with_deals_list

def get_origin_iata(city) -> str:
    data_file = "data.json"
    refresh_data = False
    city = lower(city)

    if os.path.exists(data_file) and os.path.getsize(data_file) and not refresh_data:
        with open(data_file) as f:
            data = json.load(f)
            iata = data.get(city)
            if iata is not None:
                print(time.strftime("%d-%b-%Y %I:%M:%S %p"), "-> Getting origin iata code from", data_file)
                return  iata

    print(time.strftime("%d-%b-%Y %I:%M:%S %p"), "-> Getting origin iata code from amadeus...")
    iata = get_iatacode(city)

    if iata == "":
        return ""

    try:
        with open(data_file) as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data[city] = iata

    with open(data_file, "w") as f:
        json.dump(data, f, indent=2)

    return iata


origin_city = "Bengaluru"
origin_iata = get_origin_iata(origin_city)
departure_on = time.strftime("%Y-%m-%d")

if origin_iata != "":
    # destinations stored in gsheet
    destinations = get_destinations()
    # destinations in gsheet that have deals
    destinations_with_deals = get_destinations_with_deals(destinations_list=destinations,
                                                      from_iatacode=origin_iata,
                                                      departure_date=departure_on)

    users = get_users()

    if len(destinations_with_deals) > 0:
        # print(destinations_with_deals)
        send_alerts(users=users, offers=destinations_with_deals)
    else:
        print("No deals available at the moment!")
else:
    print(f"IATA code not available for {origin_city}")


def humanize_time(value: float):
    intervals = {
        "days": 24*60*60,
        "hours": 60*60,
        "minutes": 60,
        "seconds": 1,
    }

    days, remainder = divmod(value, intervals["days"])
    hours, remainder = divmod(remainder, intervals["hours"])
    minutes, remainder = divmod(remainder, intervals["minutes"])
    seconds = round(remainder, 2)

    part = []
    if days:
        part.append(f"{int(days)} {'days' if days > 1 else 'day'}")
    if hours:
        part.append(f"{int(hours)} {'hrs' if hours > 1 else 'hr'}")
    if minutes:
        part.append(f"{int(minutes)} {'mins' if minutes > 1 else 'min'}")
    if seconds:
        part.append(f"{seconds} {'secs' if seconds != 1 else 'sec'}")

    print(" ".join(part))

end_time = time.time()
humanize_time(end_time - start_time)