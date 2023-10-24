#!/usr/bin/python3
"""10-hbnb_filters
Starts a Flask web application.
listens on 0.0.0.0, port 5000.
Routes:
    /hbnb_filters: Displays a HTML Hbnb filters page.
"""
from models import storage
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """Displays the main HBnB filters HTML page."""
    state_data = storage.all("State").values()
    amenities_data = storage.all("Amenity").values()
    return render_template("10-hbnb_filters.html",
                           states=state_data, amenities=amenities_data)


@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
