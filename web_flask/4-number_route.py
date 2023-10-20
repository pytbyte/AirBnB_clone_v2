#!/usr/bin/python3
"""4-number_route

A Flask application serves a multiple pages.
The application listens on 0.0.0.0, port 5000.

Routes:
    /: Displays a friendly 'Hello HBNB!' message.
    /hbnb: Displays a friendly 'HBNB' message.
    /c/<text>: Displays “C ” followed by the value of the text variable.
    /python: Displays “Python is cool” message.
    /python/<text>: Displays “Python” followed by the value of text variable.
    /number/<n>: Displays “n is a number” only if n is an intege
"""

from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """ friendly 'Hello HBNB!' message"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """friendly 'HBNB' message"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_is_fun(text):
    """Displays “C ” followed by the value of the text variable"""
    return "C " + text.replace("_", " ")


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_is_cool(text="is cool"):
    """Displays 'Python ' followed by the value of the text variable."""
    return "Python " + text.replace("_", " ")


@app.route("/number/<int:n>", strict_slashes=False)
def number(n):
    """Displays 'n is a number' if n is an integer."""
    return f"{n} is a number"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
