import requests
from textblob import TextBlob
import os

NEWS_API_KEY = os.getenv('NEWS_API_KEY')


# Function to fetch tennis news
def fetch_tennis_news():
    url = f"https://newsapi.org/v2/everything?q=tennis&language=en&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching news: {response.status_code}")


# Function to analyze sentiment of news content
def analyze_sentiment(content):
    blob = TextBlob(content)
    return blob.sentiment.polarity  # Sentiment score from -1 to 1


# Function to process the news data and return a list of articles with sentiment analysis
def fetch_and_process_news():
    news_data = fetch_tennis_news()

    articles = news_data.get("articles", [])
    processed_articles = []

    for article in articles:
        title = article.get("title", "No Title")
        url = article.get("url", "")
        content = article.get("content", "")
        source_name = article.get("source", {}).get("name", "Unknown")
        published_at = article.get("publishedAt", "")

        sentiment_score = analyze_sentiment(content)

        processed_articles.append({
            "title": title,
            "url": url,
            "source": source_name,
            "sentiment": sentiment_score,
            "published_at": published_at
        })

    return processed_articles
