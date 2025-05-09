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


@app.route('/rawcsv')
def get_rawcsv():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = '''
         SELECT crime_times.date_occ, locations.location, crime_types.crm_cd_desc, 
                crimes.vict_age, crimes.vict_sex, crimes.premis_desc
        FROM crimes
        JOIN crimes_crime_types_crimes_times_locations ON crimes.id = crimes_crime_types_crimes_times_locations.crime_id
        JOIN crime_types ON crime_types.id = crimes_crime_types_crimes_times_locations.crime_type_id
        JOIN crime_times ON crime_times.id = crimes_crime_types_crimes_times_locations.crime_time_id
        JOIN locations ON locations.id = crimes_crime_types_crimes_times_locations.location_id;
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
        writer.writerow(['date', 'area', 'type', 'victim_age', 'victim_sex', 'location'])
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
    start_date = request.args.get('start_date', None)
    end_date = request.args.get('end_date', None)
    area = request.args.get('area', None)
    crime_type = request.args.get('type', None)

    crimes = []
    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = '''
        SELECT crime_times.date_occ, locations.location, crime_types.crm_cd_desc, 
               crimes.vict_age, crimes.vict_sex, crimes.premis_desc
        FROM crimes
        JOIN crimes_crime_types_crimes_times_locations ON crimes.id = crimes_crime_types_crimes_times_locations.crime_id
        JOIN crime_types ON crime_types.id = crimes_crime_types_crimes_times_locations.crime_type_id
        JOIN crime_times ON crime_times.id = crimes_crime_types_crimes_times_locations.crime_time_id
        JOIN locations ON locations.id = crimes_crime_types_crimes_times_locations.location_id
        WHERE (%s IS NULL OR crime_times.date_occ >= %s) 
        AND (%s IS NULL OR crime_times.date_occ <= %s)
        '''
        params = [start_date, start_date, end_date, end_date]

        if area:
            query += ' AND LOWER(locations.location) = LOWER(%s)'
            params.append(area)

        if crime_type:
            query += ' AND LOWER(crime_types.crm_cd_desc) = LOWER(%s)'
            params.append(crime_type)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        if not rows:
            print("No records found for the given filters.", file=sys.stderr)
            return json.dumps({"message": "No records found"}), 404

        for row in rows:
            if len(row) == 6:
                crimes.append({
                    "date": row[0],
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
    help_text = """
    Crime Data API - Help

    Welcome to the Crime Data API! Below are the available endpoints and their usage:

    1. GET /
       - Description: Returns a simple welcome message.
       - Example: curl http://localhost:5000/

    2. GET /locations
       - Description: Retrieves a list of all available crime locations.
       - Example: curl http://localhost:5000/locations

    3. GET /types
       - Description: Retrieves a list of all crime types.
       - Example: curl http://localhost:5000/types

    4. GET /dates
       - Description: Retrieves a list of all recorded crime dates.
       - Example: curl http://localhost:5000/dates

    5. GET /rawcsv
       - Description: Downloads the entire crime dataset in CSV format.
       - Example: curl http://localhost:5000/rawcsv

    6. GET /crimes
       - Description: Retrieves crime data filtered by date, area, and/or crime type.
       - Query Parameters:
         - start_date: Filter crimes that occurred on or after this date.
         - end_date: Filter crimes that occurred on or before this date.
         - area: Filter crimes from a specific location.
         - type: Filter crimes by the crime type.
       - Example: curl "http://localhost:5000/crimes?start_date=2025-01-01&end_date=2025-02-01&area=Topanga&type=BATTERY%20-%20SIMPLE%20ASSAULT"

    For any issues or questions, please check the logs or contact the developers.
    """
    return help_text

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A API to get crime data')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)