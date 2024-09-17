from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class NewsArticle(db.Model):
    __tablename__ = 'news_articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False, unique=True)
    source = db.Column(db.String(100), nullable=False)
    sentiment = db.Column(db.Float, nullable=False)
    published_at = db.Column(db.String(100), nullable=False)

    def __init__(self, title, url, source, sentiment, published_at):
        self.title = title
        self.url = url
        self.source = source
        self.sentiment = sentiment
        self.published_at = published_at
