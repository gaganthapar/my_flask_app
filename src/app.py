from flask import Flask, request, jsonify
from src.tweet_fetcher import fetch_and_process_tweets

app = Flask(__name__)


@app.route("/")
def main():
    return '''
        <form action="/fetch_tweets" method="POST">
            <label>Search for tweets: </label>
            <input name="query" placeholder="Enter a keyword" required />
            <input type="submit" value="Fetch and Analyze Tweets" />
        </form>
    '''


@app.route("/fetch_tweets", methods=["POST"])
def fetch_tweets():
    query = request.form.get("query")
    result = fetch_and_process_tweets(query)
    return f"<p>{result}</p>"


if __name__ == "__main__":
    app.run(debug=True)
