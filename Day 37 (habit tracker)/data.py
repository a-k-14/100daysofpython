import requests
import webbrowser

# to build a habit tracker app where we learn about get, post, put, delete methods and
# advanced authentication

USERNAME = "ar2"
USER_TOKEN = "ydUYF736KjdbKJBfka2"
TOKEN_HEADER = {"X-USER-TOKEN": f"{USER_TOKEN}"}
GRAPH_ID = "graph-1"
# GRAPH_ID = "graph-2"


PIXELA_URL = "https://pixe.la"
PIXELA_ENDPOINT = f"{PIXELA_URL}/v1/users"
USER_PARAMETERS = {
    "token": USER_TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

# ---------Create User--------
# response = requests.post(url=PIXELA_ENDPOINT, json=USER_PARAMETERS)
# print(response.text)

# ---------Update Password-----------
# UPDATE_HEADER = {"X-USER-TOKEN": "ydUYF736KjdbKJBfkc9"}
# UPDATE_PARAMETERS = {
#     "newToken": "ydUYF736KjdbKJBfka2"
# }
# PIXELA_ENDPOINT_USER_UPDATE = f"{PIXELA_URL}/v1/users/{USER_PARAMETERS['username']}"
# update_user_response = requests.put(url=PIXELA_ENDPOINT_USER_UPDATE, headers=UPDATE_HEADER, json=UPDATE_PARAMETERS)
# print(update_user_response.text)

GRAPH_ENDPOINT = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs"
GRAPH_PARAMETERS = {
    "id": GRAPH_ID,
    "name": "Sleep",
    "unit": "hours",
    "type": "float",
    "color": "sora",
    "timezone": "Asia/Kolkata"
}
# graph_response = requests.post(url=GRAPH_ENDPOINT, headers=TOKEN_HEADER, json=GRAPH_PARAMETERS)
# print(graph_response.text)

# endpoint for post, put, delete, view
GRAPH_UPDATE_ENDPOINT = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{GRAPH_ID}"

def graph_update(date: str, quantity: str):

    # print(date.split("-"))
    # ['30', '04', '2025']
    # print(date.split("-")[::-1])
    # ['2025', '04', '30']
    # print("".join(date.split("-")[::-1]))
    # 20250430
    # date = "01-05-2025"
    # date = "".join(date.split("-")[::-1])
    date = date.replace("-", "")

    graph_update_params = {
        "quantity": quantity,
        "optionalData": '{"course": "python via udemy"}',
        "date": date
    }

    graph_update_response = requests.post(url=GRAPH_UPDATE_ENDPOINT, headers=TOKEN_HEADER, json=graph_update_params)
    # graph_update_response = requests.put(url=GRAPH_UPDATE_ENDPOINT, headers=TOKEN_HEADER, json=GRAPH_UPDATE_PARAMS)
    print(graph_update_response.text)
    print(graph_update_response.status_code)
    return graph_update_response.status_code

def delete_pixel(date: str):
    date = date.replace("-", "")
    pixel_delete_response = requests.delete(url=f"{GRAPH_UPDATE_ENDPOINT}/{date}", headers=TOKEN_HEADER)
    print(f"{GRAPH_UPDATE_ENDPOINT}/{date}")
    print(pixel_delete_response.text)
    print(pixel_delete_response.status_code)
    return pixel_delete_response.status_code

def view_graph():

    graph_view_endpoint = f"{GRAPH_UPDATE_ENDPOINT}.html?mode=simple"
    webbrowser.open_new_tab(graph_view_endpoint)
