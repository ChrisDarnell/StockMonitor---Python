import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = ""
NEWS_API_KEY = ""
TWILIO_ACCOUNT_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_PHONE = ""
SENDTO_PHONE = ""

# https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then send articles.

####

# Get yesterday's closing stock price.
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]



# Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]


# Find the difference between 1 and 2.
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"



# Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percentage_difference = round((difference / float(yesterday_closing_price)) * 100)



# If percentage is greater than .5, then get the first 3 news pieces for the COMPANY_NAME.
# https://newsapi.org/

if abs(percentage_difference) > .5:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]


# Create a list that contains the first 3 articles.
    three_articles = articles[:3]


# Create a new list of the first 3 article's headline and description.

    formatted_articles = [f"{STOCK_NAME}: {up_down}{percentage_difference}% \nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]


# Send each article as a separate message via Twilio.

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=TWILIO_PHONE,
            to=SENDTO_PHONE
        )



