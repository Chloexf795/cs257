#!/usr/bin/env python3
'''
    api.py
    Owen Xu, 21 April 2025
'''
import sys
import argparse
import flask
import json
import csv
import config
import psycopg2

app = flask.Flask(__name__)

def get_connection():
    try:
        return psycopg2.connect(database = config.database,
                                user = config.user,
                                password = config.password)
    except Exception as e:
        print(e, file=sys.stderr)
        exit()

@app.route('/locations')
def get_locations():
    locations = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = 'SELECT * FROM locations'
        print(query)
        cursor.execute(query)
        for row in cursor:
            locations.append(row[1])
    except Exception as e:
        print(e, file=sys.stderr)
    connection.close()
    return json.dumps(locations)

@app.route('/types')
def get_types():
    types = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = 'SELECT * FROM crime_types'
        cursor.execute(query)
        for row in cursor:
            types.append(row[1])
    except Exception as e:
        print(e, file=sys.stderr)
    connection.close()
    return json.dumps(types)

@app.route('/dates')
def get_dates():
    dates = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = 'SELECT * FROM crime_times'
        cursor.execute(query)
        for row in cursor:
            dates.append(row[1])
    except Exception as e:
        print(e, file=sys.stderr)
    connection.close()
    return json.dumps(dates)

@app.route('/')
def hello():
    return 'Hello, Welcome to Crime Data.'

@app.route('/help')
def get_help():
    return flask.render_template('help.html')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A API to get crime data')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)