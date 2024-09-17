from flask import Flask, jsonify, render_template
from src.models import db, NewsArticle
from src.news_fetcher import fetch_and_process_news
from src.message_queue import send_to_queue, receive_from_queue
import os

app = Flask(__name__)
#db.init_app(app)

uri = os.getenv("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


def categorize_sentiment(score):
    """Categorize the sentiment score into positive, neutral, or negative."""
    if score > 0.1:
        return "positive"
    elif score < -0.1:
        return "negative"
    else:
        return "neutral"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/fetch_news', methods=['GET'])
def fetch_news():
    try:
        new_articles = fetch_and_process_news()  # Attempt to fetch from News API
    except Exception as e:
        app.logger.error(f"Error fetching news: {str(e)}")
        new_articles = []  # Set new_articles to an empty list if there's an error

    if not new_articles:  # Check if no new articles were fetched
        db_articles = NewsArticle.query.all()  # Retrieve articles from the database
        if not db_articles:
            return jsonify({"message": "No news articles found in both API and database."}), 200

        # Convert database articles to a serializable format
        db_articles = [{
            "title": article.title,
            "url": article.url,
            "source": article.source,
            "sentiment_score": article.sentiment,  # This should still store the float score
            "sentiment_category": categorize_sentiment(article.sentiment),  # Categorize for display
            "published_at": article.published_at
        } for article in db_articles]

        return jsonify({"message": "No new articles found, displaying database articles.", "data": db_articles}), 200

    # Process and save new articles
    processed_articles = []
    for article in new_articles:
        sentiment_category = categorize_sentiment(article["sentiment_score"])  # Categorize for new articles
        if not NewsArticle.query.filter_by(url=article["url"]).first():
            news_article = NewsArticle(
                title=article["title"],
                url=article["url"],
                source=article["source"],
                sentiment=article["sentiment_score"],  # Store the float score
                published_at=article["published_at"]
            )
            db.session.add(news_article)

        # Add processed article with sentiment category to the list
        processed_articles.append({
            "title": article["title"],
            "url": article["url"],
            "source": article["source"],
            "sentiment_score": article["sentiment_score"],
            "sentiment_category": sentiment_category,  # Categorize for display
            "published_at": article["published_at"]
        })

    db.session.commit()

    return jsonify({"message": "News articles fetched and saved successfully", "data": processed_articles}), 200


if __name__ == '__main__':
    app.run(debug=False)
