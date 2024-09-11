import tweepy
from textblob import TextBlob
import psycopg2
from urllib.parse import urlparse
import os

# Twitter bearer token
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

DATABASE_URL = os.getenv('DATABASE_URL')

# Parse the connection URL
url = urlparse(DATABASE_URL)

# Connect to the PostgreSQL database
connection = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)


# Function to calculate sentiment using TextBlob
def get_sentiment(tweet_text):
    analysis = TextBlob(tweet_text)
    return analysis.sentiment.polarity


def save_to_database(tweet_id, tweet_text, tweet_created_at, user_name, sentiment):
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO tweets (id, text, created_at, user_name, sentiment) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (tweet_id, tweet_text, tweet_created_at, user_name, sentiment))
        connection.commit()
    except Exception as e:
        print(f"Error saving to database: {e}")


# Fetch tweets from Twitter using Tweepy
def fetch_and_process_tweets(query="tennis"):
    client = tweepy.Client(bearer_token=bearer_token)

    tweets = client.search_recent_tweets(query=f"{query} lang:en", max_results=10,
                                         tweet_fields=['created_at', 'text', 'author_id'])

    for tweet in tweets.data:
        tweet_id = tweet.id
        tweet_text = tweet.text
        tweet_created_at = tweet.created_at
        user_name = tweet.author_id

        # Perform sentiment analysis
        sentiment = get_sentiment(tweet_text)

        # Save tweet and sentiment to the database
        save_to_database(tweet_id, tweet_text, tweet_created_at, user_name, sentiment)

    return f"Processed {len(tweets.data)} tweets."
