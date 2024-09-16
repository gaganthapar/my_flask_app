Overview:

This project fetches news articles from an external source and saves them to the database after doing sentiment analysis. The application is built using Flask for the backend. This app is deployed on Heroku

Requirements:

Python 3.12+
PostgreSQL
Flask
Flask-migrate (for schema migrations)

Configure database:

DATABASE_URL=postgresql://username:password@localhost:5432/news_fetcher_db

Initialize the database:

Connect to your database and create the database if it doesn't exist

psql -U username -c "CREATE DATABASE news_fetcher_db;"

Apply migrations:

Initialize migrations:

flask db init

Create migrations:

flask db migrate -m "Initial migration."

Apply migrations:

flask db upgrade

Run the application:

flask run

There's a messaging queue placed between the request and the news fetcher. One more queue is placed between fetching the data and storing the data into database.

