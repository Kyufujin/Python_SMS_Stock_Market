#For more details check alpha vantage doc - https://www.alphavantage.co/documentation/#daily
#Generated api key - UXFULFGK6YBTIC6S
#Generated News Api key - bd27c4f031484cac91131226d99b368a
#DISCLAIMER - this key may be expired in the next few months
import requests
from twilio.rest import Client

STOCK_NAME = "CDR"
COMPANY_NAME = "CDPROJEKT"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "UXFULFGK6YBTIC6S"
NEWS_API_KEY = "bd27c4f031484cac91131226d99b368a"
TWILIO_SID = "ACeba9d8510360adaa6b8495695243b291"
TWILIO_AUTH_TOKEN = "c03a4ad72874c92ad240d1f6bc5c6893"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))

up_down = None
if difference > 0:
    up_down = "✅"
else:
    up_down = "❌"
diff_percent = round((difference / float(yesterday_closing_price)) * 100)

if abs(diff_percent) > 0.1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]

    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="twilioAppNumberShouldBeHere",
            to="YourNumber"
        )
#To send the message you need your own twilio number
#After that you should put in "to" field your own number.
#For more details check twilio SMS app doc - https://www.twilio.com/docs/sms/choose-the-right-phone-number-type