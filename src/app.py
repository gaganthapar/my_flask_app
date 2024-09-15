from flask import Flask, render_template

import os


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    print("Current working directory:", os.getcwd())

    app.run(debug=True)
