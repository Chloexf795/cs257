#!/usr/bin/env python3
'''
    api.py
    Owen Xu, Chloe Xufeng

    This file contains the API endpoints for the crime data visualization application.
'''
import argparse
import flask
import api

app = flask.Flask(__name__, static_folder='static', template_folder='templates')
app.register_blueprint(api.api, url_prefix='/api')

# Define the home route, which serves the index.html template
@app.route('/')
def home():
    return flask.render_template('index.html')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A tiny Flask application, including API')
    parser.add_argument('host', help='the host to run on')
    parser.add_argument('port', type=int, help='the port to listen on')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
