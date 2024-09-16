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


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/fetch_news', methods=['GET'])
def fetch_news():
    try:
        articles = fetch_and_process_news()
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
    app.run(debug=False)
