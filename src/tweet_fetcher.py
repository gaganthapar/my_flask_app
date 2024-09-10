import tweepy
import pymysql
from textblob import TextBlob

# Twitter bearer token
bearer_token = "AAAAAAAAAAAAAAAAAAAAADhnvgEAAAAAqurcrXsXDnIDOqsEI2bKDb0rZKg%3DGKzj0ajaVU4zZQMquRx4AMZLZoHukehX3RTxD1dwaeZk3sUJJi"

# MySQL Database connection
connection = pymysql.connect(
    host='localhost',
    user='your_db_user',
    password='your_db_password',
    database='twitter_db'
)

# Function to calculate sentiment using TextBlob
def get_sentiment(tweet_text):
    analysis = TextBlob(tweet_text)
    return analysis.sentiment.polarity  # Polarity is a float between -1 (negative) and 1 (positive)

# Function to save tweet data and sentiment into the database
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

    tweets = client.search_recent_tweets(query=f"{query} lang:en", max_results=10, tweet_fields=['created_at', 'text', 'author_id'])

    for tweet in tweets.data:
        tweet_id = tweet.id
        tweet_text = tweet.text
        tweet_created_at = tweet.created_at
        user_name = tweet.author_id  # Placeholder; you'd need additional requests to get the user name

        # Perform sentiment analysis
        sentiment = get_sentiment(tweet_text)

        # Save tweet and sentiment to the database
        save_to_database(tweet_id, tweet_text, tweet_created_at, user_name, sentiment)

    return f"Processed {len(tweets.data)} tweets."
