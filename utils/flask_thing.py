from flask import Flask
from threading import Thread
import os


port = int(os.getenv('PORT', 8080))

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello, I am alive!, what about you :)"


def run():
    app.run(host='0.0.0.0', port=port)


def keep_alive():
    t = Thread(target=run)
    t.start()