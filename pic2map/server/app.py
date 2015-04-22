# -*- coding: utf-8 -*-
"""Web application server."""

from flask import (
    Flask,
    render_template,
)

app = Flask(__name__)

@app.route('/')
def index():
    """Application main page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
