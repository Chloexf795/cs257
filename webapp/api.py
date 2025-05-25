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

api = flask.Blueprint('api', __name__)

def get_connection():
    try:
        return psycopg2.connect(database = config.database,
                                user = config.user,
                                password = config.password)
    except Exception as e:
        print(e, file=sys.stderr)
        exit()

@api.route('/areas')
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

@api.route('/types')
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

@api.route('/dates')
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


@api.route('/rawcsv')
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

@api.route('/crimes')
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

@api.route('/')
def hello():
    return 'Hello, Welcome to Crime Data.'

@api.route('/help')
def get_help():
    return flask.render_template('help.html')

@api.route('/charts/crimesOverTime')
def crimesOverTime():
    data = {}
    try:
        conn = get_connection()
        cur = conn.cursor()
        query = '''
            SELECT months.month, COUNT(*)
            FROM crime_events
            JOIN months ON crime_events.month_id = months.id
            GROUP BY months.month
            ORDER BY months.month
        '''
        cur.execute(query)
        for month, count in cur.fetchall():
            data[month] = count
    except Exception as e:
        print(e, file=sys.stderr)
    finally:
        conn.close()
    return json.dumps(data)

@api.route('/charts/victimAges')
def victimAges():
    buckets = {}
    try:
        conn = get_connection()
        cur = conn.cursor()
        query = '''
            SELECT vict_age FROM crimes
            WHERE vict_age IS NOT NULL AND vict_age > 0
        '''
        cur.execute(query)
        for (age,) in cur.fetchall():
            bin = (age // 10) * 10
            label = f"{bin}-{bin+9}"
            buckets[label] = buckets.get(label, 0) + 1
    except Exception as e:
        print(e, file=sys.stderr)
    finally:
        conn.close()
    return json.dumps(buckets)

@api.route('/charts/victimSex')
def victimSex():
    counts = {}
    try:
        conn = get_connection()
        cur = conn.cursor()
        query = '''
            SELECT vict_sex, COUNT(*) FROM crimes
            WHERE vict_sex IS NOT NULL AND vict_sex != ''
            GROUP BY vict_sex
        '''
        cur.execute(query)
        for sex, count in cur.fetchall():
            counts[sex] = count
    except Exception as e:
        print(e, file=sys.stderr)
    finally:
        conn.close()
    return json.dumps(counts)

@api.route('/charts/filtered')
def get_filtered_charts():
    start = request.args.get('start_month')
    end = request.args.get('end_month')
    area = request.args.get('area')
    ctype = request.args.get('type')

    counts_by_month = {"2025-01": 0, "2025-02": 0, "2025-03": 0}
    age_buckets = {}
    sex_counts = {}

    try:
        conn = get_connection()
        cur = conn.cursor()
        query = '''
            SELECT months.month, crimes.vict_age, crimes.vict_sex
            FROM crimes
            JOIN crime_events ON crimes.id = crime_events.crime_id
            JOIN months ON crime_events.month_id = months.id
            JOIN areas ON crime_events.area_id = areas.id
            JOIN types ON crime_events.type_id = types.id
            WHERE (%s IS NULL OR months.month >= %s)
              AND (%s IS NULL OR months.month <= %s)
              AND (%s IS NULL OR LOWER(areas.area) = LOWER(%s))
              AND (%s IS NULL OR LOWER(types.type) = LOWER(%s))
        '''
        params = [start, start, end, end, area, area, ctype, ctype]
        cur.execute(query, params)

        for month, age, sex in cur.fetchall():
            # Month count
            if month in counts_by_month:
                counts_by_month[month] += 1

            # Age bucket
            if age is not None and isinstance(age, (int, float)) and age > 0:
                bucket = f"{(int(age)//10)*10}-{(int(age)//10)*10+9}"
                age_buckets[bucket] = age_buckets.get(bucket, 0) + 1

            # Sex count
            if sex:
                sex_counts[sex] = sex_counts.get(sex, 0) + 1

        # Sort age buckets by age range
        sorted_age_buckets = dict(sorted(age_buckets.items(), 
                                       key=lambda x: int(x[0].split('-')[0])))

    except Exception as e:
        print(f"Error in filtered chart API: {e}", file=sys.stderr)
        return json.dumps({"error": str(e)}), 500
    finally:
        conn.close()

    return json.dumps({
        "month_counts": counts_by_month,
        "age_buckets": sorted_age_buckets,
        "sex_counts": sex_counts
    })


if __name__ == '__main__':
    parser = argparse.ArgumentParser('A API to get crime data')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    api.run(host=arguments.host, port=arguments.port, debug=True)