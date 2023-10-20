#!/usr/bin/python3
"""1-hbnb_route

A Flask application serves a multiple pages.
The application listens on 0.0.0.0, port 5000.

Routes:
    /: Displays a friendly 'Hello HBNB!' message.
    /hbnb: Displays a friendly 'HBNB' message
"""

from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """friendly 'Hello HBNB!' message"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """friendly 'HBNB' message"""
    return "HBNB"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
