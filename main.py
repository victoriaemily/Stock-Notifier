import requests
from datetime import datetime
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla"
STOCK_API_KEY = "7INSERT YOUR API"
NEWS_API_KEY = "INSERT YOUR API"
STOCK_URL = "https://www.alphavantage.co/query"
NEWS_URL = "https://newsapi.org/v2/top-headlines"

ACCT_SID = "TWILIO SID"
AUTH_TOKEN = "TWILIO TOKEN"

PARAMETERS = {
    'function': "TIME_SERIES_DAILY",
    'symbol': STOCK,
    'apikey': STOCK_API_KEY,
    
}
## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
request = requests.get(STOCK_URL, PARAMETERS)
data = request.json()
stock_per_day = data["Time Series (Daily)"]

time_now = str(datetime.now())
date_now = time_now[:10]
yesterday_date = date_now[:8] + str(int(date_now[8:10]) -1)
day_before_date = date_now[:8] + str(int(date_now[8:10]) -2)


yesterday_close_price = float(stock_per_day[yesterday_date]["4. close"])
day_before_close_price = float(stock_per_day[day_before_date]["4. close"])

change = (yesterday_close_price-day_before_close_price)/day_before_close_price

if abs(change) >= .05:
    getNews = True

if getNews == True:
    NEWS_PARAMS = {
        'apiKey': NEWS_API_KEY,
        'q': COMPANY_NAME,
        'from': day_before_date,
        'to': yesterday_date,
        'sortBy': 'popularity',
    }

    #fetching headlines
    
    request = requests.get(NEWS_URL,NEWS_PARAMS)
    data = request.json()

    headlines = []
    briefs = []
    if change < 0:
        emote = '⬇️'
    else:
        emote = '⬆️'
    articles = data['articles'][0:3]
    article_string = ''
    for article in articles:
        article_string += '\n' + '---------------------' + '\n' + article['title'] + '\n' + article['description'] 
    
    #now uses twilio to send message
    
    client = Client(ACCT_SID, AUTH_TOKEN)
    message = client.messages \
         .create(
         body=f"{STOCK}: {emote}{change*100}%{article_string}",
         from_='+19853797328',
         to='+18323404253'
     )
    