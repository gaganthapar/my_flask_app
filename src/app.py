from flask import Flask, jsonify
from models import db, NewsArticle
from news_fetcher import fetch_and_process_news
import os

app = Flask(__name__)

# Configure PostgreSQL Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.getenv("DATABASE_URL", "postgresql://localhost/news_db"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create database tables
@app.before_first_request
def create_tables():
    db.create_all()

# Fetch news articles and save to the database
@app.route('/fetch_news', methods=['GET'])
def fetch_news():
    try:
        articles = fetch_and_process_news()

        # Save articles to the database, skipping duplicates
        for article in articles:
            if not NewsArticle.query.filter_by(url=article["url"]).first():
                news_article = NewsArticle(
                    title=article["title"],
                    url=article["url"],
                    source=article["source"],
                    sentiment=article["sentiment"],
                    published_at=article["published_at"]
                )
                db.session.add(news_article)

        db.session.commit()

        return jsonify({"message": "News articles fetched and saved successfully", "data": articles}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
