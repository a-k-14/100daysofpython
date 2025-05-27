# GOAL
# get the list of places and flight ticket prices recorded in gsheet
# check if there are any dates where the flight ticket prices for these places is less than the price in gsheet
# if yes, send a sms notification to the user
import json
import time
import requests
import os
import pandas as pd
from amadeus import Client, ResponseError
from alerts import send_sms
import datetime as dt

# amadeus API info
AMADEUS_CLIENT_ID = "FQbZYnJVAPrjw8MHwgNf62lZKGuDpiU0"
AMADEUS_CLIENT_SECRET = "HAM5IGs8gFcdOKz1"

amadeus_client = Client(client_id=AMADEUS_CLIENT_ID, client_secret=AMADEUS_CLIENT_SECRET)


# get the destinations list stored in gsheet via sheety and store in csv
def get_destinations() -> list:
    file_name = "destinations.csv"
    should_refresh = False

    sheety_get_endpoint = "https://api.sheety.co/ea02cd191d3ecb59125868bb40d3367e/flightDeals/prices"
    sheety_token = "sjv6^#Y12904B[:23fdfxzx"
    sheety_header = {
        "Authorization": f"Bearer {sheety_token}"
    }
    sheety_put_endpoint = "https://api.sheety.co/ea02cd191d3ecb59125868bb40d3367e/flightDeals/prices/"

    # get the list from gsheet only if the csv file does not exist, is empty or should_refresh is true
    if os.path.exists(file_name) and os.path.getsize(file_name) > 0 and not should_refresh:
        df = pd.read_csv(file_name) # this gives a dict
        # return the dict as list with this
        # print(df.to_dict(orient="records"))
        d_list = df.to_dict(orient="records")
        return d_list

    else:
        print("Getting data from gsheet via sheety")
        sheety_response = requests.get(url=sheety_get_endpoint, headers=sheety_header)
        sheety_response.raise_for_status()

        if sheety_response.status_code != 200:
            print(sheety_response.text)

        d_list = sheety_response.json()["prices"]
        for item in d_list:
            if item["iataCode"] == "":
                item["iataCode"] = get_iatacode(item["city"])

                # update the gsheet with iata code
                sheety_payload = {
                    "price": {
                        "iataCode": item["iataCode"],
                    }
                }
                sheety_put_response = requests.put(
                    url=f"{sheety_put_endpoint}/{item['id']}",
                    headers=sheety_header,
                    json=sheety_payload
                )
                print(sheety_put_response.status_code)

        pd.DataFrame(d_list).to_csv(file_name, index=False)
        # print(d_list)
        return d_list


# get new amadeus access if old one expired or if it does not exist already
def get_new_access_token() -> dict:
    """
    get a new access token from amadeus and return the same
    :return: {"access_token": value, "expires_in": value}
    """
    token_request_endpoint = "https://test.api.amadeus.com/v1/security/oauth2/token"
    token_request_header = {
        "grant_type": "client_credentials",
        "client_id": AMADEUS_CLIENT_ID,
        "client_secret": AMADEUS_CLIENT_SECRET,
    }
    token_request_response = requests.post(url=token_request_endpoint, data=token_request_header)
    response_data = token_request_response.json()
    print(response_data)
    token_data = {
        "access_token": response_data["access_token"],
        "expires_in": response_data["expires_in"],
    }
    # print(token_data)

    return token_data


# retrieve an already stored amadeus api token or fetch new token if not stored
def retrieve_access_token():
    # check if json file exists
    file_name = "data.json"

    if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
        with open(file_name) as f:
            token_data = json.load(f)

        if time.time() < token_data["expires_at"]:
            return token_data["access_token"]

    # if we have reached here means either json doesn't exist or token validity expired
    token_data = get_new_access_token()
    # add expires_at instead of expires_in, and logged_at to token_data
    token_data_for_json = {
        "access_token": token_data["access_token"],
        "expires_at": time.time() + (token_data["expires_in"] - 60),
        "logged_at": time.strftime("%d-%b-%Y %I:%M:%S %p")
    }
    with open(file_name, "w") as f:
        json.dump(token_data_for_json, f, indent=2)
    return token_data["access_token"]


# to get the IATA code for destinations, from amadeus API
def get_iatacode(city: str):
    # this is requests method
    # amadeus_server = "https://test.api.amadeus.com/v1"
    # get_city_endpoint = "/reference-data/locations/cities"
    # get_city_params = {
    #     "keyword": city,
    #     "max": 1,
    # }
    # amadeus_header = {
    #     "Authorization": F"Bearer {retrieve_access_token()}"
    # }
    # print(amadeus_header)
    #
    # response = requests.get(url=f"{amadeus_server}{get_city_endpoint}", params=get_city_params, headers=amadeus_header)
    # response.raise_for_status()
    # data = response.json()
    # print(data)

    city = city if len(city) <= 10 else city[:10]

    try:
        response = amadeus_client.reference_data.locations.cities.get(keyword=city)
        data = response.data
        print(data)
        iatacode = data[0]["iataCode"]
        return iatacode

    except ResponseError as err:
        print(err.description)
        # raise err
        return ""


# send alerts if the current prices are lower than the prices in the gsheet
def get_alert(destination: str, max_price: int):
    # this is not working
    # try:
    #     response = amadeus_client.shopping.flight_dates.get(origin='LCY', destination='NYC', departureDate="2025-05-20")
    #     print(response.data)
    # except ResponseError as e:
    #     print(e.description)
    #     raise e
    base_url = "https://test.api.amadeus.com/v2"
    get_endpoint = "/shopping/flight-offers"
    token_header = {
        "Authorization": F"Bearer {retrieve_access_token()}"
    }
    params = {
        "originLocationCode": "BLR",
        "destinationLocationCode": destination,
        "departureDate": (dt.datetime.now() + dt.timedelta(10)).strftime("%Y-%m-%d"),
        "adults": 1,
        "max": 1
    }

    response = requests.get(url=f"{base_url}{get_endpoint}", headers=token_header, params=params)
    response.raise_for_status()
    data = response.json()["data"][0]
    print(data)
    price_segment = data["price"]
    price = float(price_segment['total'])
    if price <= max_price:
        currency = price_segment['currency']
        dep_date = data["lastTicketingDate"]
        dep_iata = data["itineraries"][0]["segments"][0]["departure"]["iataCode"]
        dest_iata = data["itineraries"][0]["segments"][-1]["arrival"]["iataCode"]

        alert= f"Low price alert! Only {currency}: {price} to fly from {dep_iata} to {dest_iata}, on {dep_date}."
        print(alert)
        return alert

    return ""

# list of destination from gsheet
destinations_list = get_destinations()
# print(destinations_list)
for item in destinations_list:
    alert_to_send = get_alert(destination=item["iataCode"], max_price=item["lowestPrice"])
    if alert_to_send != "":
        # send_sms(alert_to_send)
        ...