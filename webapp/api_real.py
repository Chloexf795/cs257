#!/usr/bin/env python3
'''
    api.py
    Owen Xu, Chloe Xufeng

'''
import sys
import argparse
import flask
import json
import csv
import config
import psycopg2
from flask import request, Response

app = flask.Flask(__name__)

def get_connection():
    try:
        return psycopg2.connect(database = config.database,
                                user = config.user,
                                password = config.password)
    except Exception as e:
        print(e, file=sys.stderr)
        exit()

@app.route('/areas')
def get_areas():
    areas = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = 'SELECT * FROM areas'
        print(query)
        cursor.execute(query)
        for row in cursor:
            areas.append(row[1])
    except Exception as e:
        print(e, file=sys.stderr)
    connection.close()
    return json.dumps(areas)

@app.route('/types')
def get_types():
    types = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = 'SELECT * FROM types'
        cursor.execute(query)
        for row in cursor:
            types.append(row[1])
    except Exception as e:
        print(e, file=sys.stderr)
    connection.close()
    return json.dumps(types)

@app.route('/months')
def get_months():
    months = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = 'SELECT * FROM months'
        cursor.execute(query)
        for row in cursor:
            months.append(row[1])
    except Exception as e:
        print(e, file=sys.stderr)
    connection.close()
    return json.dumps(months)


@app.route('/rawcsv')
def get_rawcsv():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = '''
            SELECT months.month, areas.area, types.type,
                   crimes.vict_age, crimes.vict_sex, crimes.location
            FROM crimes
            JOIN crime_events ON crimes.id = crime_events.crime_id
            JOIN types ON types.id = crime_events.type_id
            JOIN months ON months.id = crime_events.month_id
            JOIN areas ON areas.id = crime_events.area_id;
        '''
        cursor.execute(query)
        rows = cursor.fetchall()
    except Exception as e:
        print(f"Error generating CSV: {e}", file=sys.stderr)
        return "Database error", 500
    finally:
        if 'connection' in locals():
            connection.close()

    def generate():
        output = csv.StringIO()
        writer = csv.writer(output)
        writer.writerow(['month', 'area', 'type', 'victim_age', 'victim_sex', 'location'])
        yield output.getvalue()
        output.seek(0)
        output.truncate(0)

        for row in rows:
            writer.writerow(row)
            yield output.getvalue()
            output.seek(0)
            output.truncate(0)

    return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=crime_data.csv"})

@app.route('/crimes')
def get_crimes():
    start_month = request.args.get('start_month', None)
    end_month = request.args.get('end_month', None)
    area = request.args.get('area', None)
    crime_type = request.args.get('type', None)

    crimes = []
    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = '''
            SELECT months.month, areas.area, types.type,
                   crimes.vict_age, crimes.vict_sex, crimes.location
            FROM crimes
            JOIN crime_events ON crimes.id = crime_events.crime_id
            JOIN types ON types.id = crime_events.type_id
            JOIN months ON months.id = crime_events.month_id
            JOIN areas ON areas.id = crime_events.area_id
            WHERE (%s IS NULL OR months.month >= %s) 
            AND (%s IS NULL OR months.month <= %s)
        '''
        params = [start_month, start_month, end_month, end_month]

        if area:
            query += ' AND LOWER(areas.area) = LOWER(%s)'
            params.append(area)

        if crime_type:
            query += ' AND LOWER(types.type) = LOWER(%s)'
            params.append(crime_type)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        if not rows:
            print("No records found for the given filters.", file=sys.stderr)
            return json.dumps({"message": "No records found"}), 404

        for row in rows:
            if len(row) == 6:
                crimes.append({
                    "month": row[0],
                    "area": row[1],
                    "type": row[2],
                    "victim_age": row[3],
                    "victim_sex": row[4],
                    "location": row[5]
                })
            else:
                print(f"Unexpected row format: {row}", file=sys.stderr)

    except Exception as e:
        print(f"Error retrieving crimes: {e}", file=sys.stderr)
        return "Database error", 500
    finally:
        connection.close()
    return json.dumps(crimes)

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