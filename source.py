import json
import pandas as pd
import time
from datetime import date
from newsapi import NewsApiClient
from nltk.sentiment import SentimentIntensityAnalyzer

portfolio = json.load(open("portfolio.json"))

def get_portfolio_status():
        """
        get_portfolio_status() reads the portfolio, fetches last day's stock price details from Yahoo Finance and calculates the net and individual profits.
        It returns a dictionary with total_profit and individual profit for each ticker.
        """

        def get_profit(stock, data):
                total_spent = 0
                num_stocks = 0
                for holding in stock["holding"]:
                        total_spent += holding[0] * holding[1]
                        num_stocks += holding[0]

                market_price = num_stocks * float(data["Close"])
                return market_price - total_spent

        time_end = int(time.mktime(date.today().timetuple()))
        time_start = time_end - 86400*2
        portfolio_status = {"total": 0}

        for stock in portfolio["portfolio"]:
                portfolio_status[stock["ticker"]] = []
                query = f"https://query1.finance.yahoo.com/v7/finance/download/META?period1={time_start}&period2={time_end}&interval=1d&events=history&includeAdjustedClose=true"
                data = pd.read_csv(query)
                profit = get_profit(stock, data)
                portfolio_status["total"] += profit

                portfolio_status[stock["ticker"]] = {"profit": profit, "open":float(data["Open"]), "close":float(data["Close"])}

        return portfolio_status


def get_portfolio_news():
        """
        get_portfolio_news() first gets NEWS related to the stock and runs sentiment analysis on it.
        It returns a dictionary with ticker name as the key and NEWS with it's media sentiment as the value for each stock.
        """

        def get_sentiment(news):
                sia = SentimentIntensityAnalyzer()
                polarity_score = sia.polarity_scores(news)["compound"]
                return polarity_score

        def get_news(stock_name):
                newsapi = NewsApiClient(api_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
                response = newsapi.get_top_headlines(q=stock_name, language='en')["articles"][:3]
                top_headlines = [[news["title"], -1 if get_sentiment(news["title"]) < 0 else 1, news["url"]] for news in response]
                return top_headlines

        portfolio_news = {}
        for stock in portfolio["portfolio"]:
                portfolio_news[stock["ticker"]] = get_news(stock["name"])
        return portfolio_news


def get_stock_summary():
        """
        get_stock_summary() is the driver function of this project. It fetches stock details and related news with media sentiment, and finally displays it to the user.
        """
        def display_summary(details, news):
                print(f"\nNet Profit with the Portfolio: ${details['total']}", "\n\n")
                print("Individual Stock Summary:\n")
                for stock in details.keys():
                        if stock == "total":
                                continue
                        print(f'\t{stock} | Open: {details[stock]["open"]} | Close: {details[stock]["close"]} | Profit: {details[stock]["profit"]}')
                        sentiment_score = 0
                        for sentiment in news[stock]:
                                sentiment_score += sentiment[1]
                        print(f'\t(Media sentiment for {stock} is {"POSITIVE" if sentiment_score >= 0 else "NEGATIVE"})')
                        for url in news[stock]:
                                print(f"\t\t> {url[2]}")
                        print("\n")


        stock_details = get_portfolio_status()
        news = get_portfolio_news()
        display_summary(stock_details, news)


if __name__ == "__main__":
    get_stock_summary()