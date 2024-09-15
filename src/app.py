from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    print("Current working directory:", os.getcwd())
    print("Files in the current directory:", os.listdir())
    print("Files in 'templates' directory:", os.listdir('templates'))

    app.run(debug=True)
