## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

## STEP 3: Use https://www.twilio.com
# Send a separate message with the percentage change and each article's title and description to your phone number.


#Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

import requests
from twilio.rest import Client

# ---------------stock prices API------------------
COMPANY_NAME = "Microsoft"
STOCK_SYMBOL = "MSFT"
STOCK_API_KEY = "UKQNYPNDHDD69V2H"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_PARAMETERS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_SYMBOL,
    "apikey": STOCK_API_KEY
}

# ---------------news API------------------
NEWS_API_KEY = "b6f1cad97c19487684fe1ff292fc4fba"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_PARAMETERS = {
    "q": COMPANY_NAME,
    "language": "en",
    "sortBy": "relevancy",
    "apiKey": NEWS_API_KEY
}

# ---------------twilio API------------------
# AC896131eb83cf52f4568c9e7ca5ca8a35
# ACa40383604d5f33c6267353c79111bbd8
ACCOUNT_SID = "ACa40383604d5f33c6267353c79111bbd8"
# 21326ca5d58e307c182f987d6e394c8f
# 014b46aacfb5e521b0d549e4c29b1755
AUTH_TOKEN = "014b46aacfb5e521b0d549e4c29b1755"
# +13185438874
# +17627585633
VIRTUAL_TWILIO_NUM = "+17627585633"
VERIFIED_NUM = "+917019467824"

def get_stock_movement():
    """
    Gets the stock prices for the symbol specified, for yesterday and the day before and,
    returns the change in stock closing prices between the 2 days
    :return: change in stock price in %
    """

    stock_price_response = requests.get(url=STOCK_ENDPOINT, params=STOCK_PARAMETERS)
    stock_price_response.raise_for_status()
    # print(stock_price_response.text)

    # default structure of the json is dict
    # {'Meta Data': {'1. Information': 'Daily Prices (open, high, low, close) and Volumes', '2. ....}, 'Time Series (Daily)': {'2025-04-28': {'1. open': '232.8600'....,
    stock_data_dict = stock_price_response.json()
    # print(data_dict)

    # we need to get the first 2 key values inside the value of key "Time Series (Daily)"
    # get the value of key "Time Series (Daily)" as items (key-value pairs) grouped as a list tuple
    # [('key', 'value'), ('key', 'value')...]
    # [('2025-04-28', {'1. open': '232.8600', '2. high': '236.6300', '3. low': '232.0700', '4. close': '236.1600', '5. volume': '3653461'}),
    stock_data_list = list(stock_data_dict["Time Series (Daily)"].items())
    # print(data_list)

    # slice the data_list to get the first 2 items
    first_two_items = stock_data_list[0:2]
    # print(first_two_items)

    # get the day 1 close (day before yesterday) and day 2 (yesterday) close as float
    price_t_minus_1 = first_two_items[0][1]["4. close"]
    price_t_minus_1 = float(price_t_minus_1)

    price_t_minus_2 = float(first_two_items[1][1]["4. close"])

    # change of stock price between yesterday and the day before
    movement = round( (price_t_minus_1 - price_t_minus_2) / price_t_minus_2 * 100, 2) + 10
    return movement

def get_news_articles():
    """
    Gets the latest news related to the company and returns 2 news articles with title & brief
    :return: dict of 3 latest articles with 'title' and 'brief'
    """
    news_response = requests.get(url=NEWS_ENDPOINT, params=NEWS_PARAMETERS)
    # print(news_response.url)
    news_response.raise_for_status()
    news_data = news_response.json()
    news_articles_raw = news_data["articles"][0:3]

    articles = []
    for item in news_articles_raw:
        article = {
            "headline": item["title"],
            "brief": item["description"]
        }
        articles.append(article)

    return articles


def send_alert(articles, movement):
    """
    Send sms alert of 3 latest news articles if the stock movement is +/- 5%
    :return: None
    """

    icon = "🔺" if movement > 0 else "🔻"

    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    for item in articles:
        # as we get length exceeding error, we ensure total message len in under 300
        max_len = 320 - 50
        head = f'{STOCK_SYMBOL}: {movement}%\nHeadline: {item["headline"]}.\n'
        brief = f'Brief: {item["brief"]}.'

        available_len_for_brief = max_len - len(head)

        if available_len_for_brief < 0 :
            head = head[:max_len]
            brief = ""
        else:
            brief = brief[:available_len_for_brief]

        message = client.messages.create(
            from_= VIRTUAL_TWILIO_NUM,
            to= VERIFIED_NUM,
            body= head + brief
        )
        print(len(message.body))
        print(message.status)


stock_movement = get_stock_movement()
print(stock_movement)
if abs(stock_movement) > 5:
    news_articles = get_news_articles()
    # print(news_articles)
    send_alert(news_articles, 10)