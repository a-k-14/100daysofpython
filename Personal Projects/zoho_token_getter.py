# GOAL
# to get access + refresh token from zoho for pushing IIMBAA data from excel
import requests
import os


url = "https://accounts.zoho.in/oauth/v2/token"
params = {
    "code": os.environ.get("code"),
    "client_id": os.environ.get("client_id"),
    "client_secret": os.environ.get("client_secret"),
    "redirect_uri": "https://www.zoho.com/books",
    "grant_type": "authorization_code",
}

print(params)

response = requests.post(url, params=params)
response.raise_for_status()
print(response.content)