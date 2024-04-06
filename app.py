from flask import Flask, request, render_template, jsonify
from newsapi import NewsApiClient
import yfinance as yf
from news_analysis import sample_analyze_entity_sentiment as smes

app = Flask(__name__)

tech_giants = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Amazon': 'AMZN',
    'Google': 'GOOGL',
    'Facebook': 'FB',
    'Tesla': 'TSLA',
    'Nvidia': 'NVDA',
    'Intel': 'INTC',
    'Adobe': 'ADBE',
    'Netflix': 'NFLX'
}

# Initialize the NewsAPI client with your API key
newsapi = NewsApiClient(api_key='777ba1e789914d5f8aa4444caf3dcb6e')

# List of major tech companies
tech_companies = ['Apple', 'Microsoft', 'Amazon', 'Google', 'Facebook', 'Netflix', 'Tesla', 'IBM', 'Intel', 'Nvidia']


@app.route('/get_stock_data', methods=['POST'])
def get_stock_data():
    article_title = request.json.get('article_title')
    companies_mentioned = []
    for company, ticker in tech_giants.items():
        if company.lower() in article_title.lower():
            companies_mentioned.append((company, ticker))

    if companies_mentioned:
        stock_data = {}
        for company, ticker in companies_mentioned:
            stock_data[ticker] = yf.Ticker(ticker).history()

        formatted_data = {
            "stock_data": process_stock_data(stock_data),
            "sentiment_data": smes(article_title)
        }

        return jsonify(formatted_data)
    else:
        return jsonify({'error': 'Company not found'})


def process_stock_data(stock_data):
    all_stock_data = []
    for ticker, data in stock_data.items():
        data = {
            'ticker': ticker,
            'dates': data.index.tolist(),
            'close_prices': data['Close'].tolist()
        }
        all_stock_data.append(data)
    return all_stock_data


if __name__ == '__main__':
    app.run(debug=True)
