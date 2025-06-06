#!/usr/bin/env python3
'''
    api.py
    Owen Xu, Chloe Xufeng

    This file contains the API endpoints for the crime data visualization application.
'''
import sys
import argparse
import flask
import json
import csv
import config
import psycopg2
from flask import request, Response
import re

api = flask.Blueprint('api', __name__)

def get_connection():
    '''
    Creates and returns a connection to the PostgreSQL database using config parameters.
    Returns: psycopg2 connection object
    '''
    try:
        return psycopg2.connect(database=config.database,
                               user=config.user,
                               password=config.password)
    except Exception as e:
        print(e, file=sys.stderr)
        return None

@api.route('/areas')
def get_areas():
    '''Returns a list of all unique areas in the dataset'''
    try:
        connection = get_connection()
        if not connection:
            return json.dumps({"error": "Database connection failed"}), 500
        
        cursor = connection.cursor()
        query = 'SELECT * FROM areas ORDER BY area ASC'
        cursor.execute(query)
        areas = [row[1] for row in cursor]
        connection.close()
        
        if not areas:
            return json.dumps({"error": "No areas found"}), 404
            
        return json.dumps(areas)
    except Exception as e:
        print(e, file=sys.stderr)
        return json.dumps({"error": "Internal server error"}), 500

@api.route('/types')
def get_types():
    '''Returns a list of all crime types in the dataset'''
    try:
        connection = get_connection()
        if not connection:
            return json.dumps({"error": "Database connection failed"}), 500
            
        cursor = connection.cursor()
        query = 'SELECT * FROM types ORDER BY type ASC'
        cursor.execute(query)
        types = [row[1] for row in cursor]
        connection.close()
        
        if not types:
            return json.dumps({"error": "No crime types found"}), 404
            
        return json.dumps(types)
    except Exception as e:
        print(e, file=sys.stderr)
        return json.dumps({"error": "Internal server error"}), 500

@api.route('/dates')
def get_months():
    '''Returns a sorted list of all months in the dataset'''
    try:
        connection = get_connection()
        if not connection:
            return json.dumps({"error": "Database connection failed"}), 500
            
        cursor = connection.cursor()
        query = 'SELECT month FROM months ORDER BY month ASC'
        cursor.execute(query)
        months = [row[0] for row in cursor]
        connection.close()
        
        if not months:
            return json.dumps({"error": "No dates found"}), 404
            
        return json.dumps(months)
    except Exception as e:
        print(e, file=sys.stderr)
        return json.dumps({"error": "Internal server error"}), 500

@api.route('/rawcsv')
def get_rawcsv():
    '''
    Generates and returns a CSV file containing all crime data.
    The CSV includes: month, area, type, victim age, victim sex, and location.
    '''
    try:
        connection = get_connection()
        if not connection:
            return json.dumps({"error": "Database connection failed"}), 500
            
        cursor = connection.cursor()
        query = '''
            SELECT months.month, areas.area, types.type,
                   crimes.vict_age, crimes.vict_sex, crimes.location
            FROM crimes
            JOIN crime_events ON crimes.id = crime_events.crime_id
            JOIN types ON types.id = crime_events.type_id
            JOIN months ON months.id = crime_events.month_id
            JOIN areas ON areas.id = crime_events.area_id
            ORDER BY months.month ASC;
        '''
        cursor.execute(query)
        rows = cursor.fetchall()
        
        if not rows:
            return json.dumps({"error": "No data found"}), 404
            
    except Exception as e:
        print(f"Error generating CSV: {e}", file=sys.stderr)
        return json.dumps({"error": "Internal server error"}), 500
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

    return Response(generate(), 
                   mimetype='text/csv',
                   headers={"Content-Disposition": "attachment;filename=crime_data.csv"})

@api.route('/crimes')
def get_crimes():
    '''
    Returns filtered crime data based on query parameters:
    - start_month: Start of date range
    - end_month: End of date range
    - area: Specific area to filter by
    - type: Specific crime type to filter by
    '''
    start_month = request.args.get('start_month', None)
    end_month = request.args.get('end_month', None)
    area = request.args.get('area', None)
    crime_type = request.args.get('type', None)

    date_pattern = r'^\d{4}-\d{2}$'
    
    # Validate date format if provided
    if start_month and not re.match(date_pattern, start_month):
        return json.dumps({"error": "Invalid start_month format. Use YYYY-MM"}), 400
    if end_month and not re.match(date_pattern, end_month):
        return json.dumps({"error": "Invalid end_month format. Use YYYY-MM"}), 400

    try:
        connection = get_connection()
        if not connection:
            return json.dumps({"error": "Database connection failed"}), 500
            
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

        query += ' ORDER BY months.month ASC'
        cursor.execute(query, params)
        rows = cursor.fetchall()

        if not rows:
            return json.dumps({"message": "No records found for the given criteria"}), 404

        crimes = []
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
        return json.dumps({"error": "Internal server error"}), 500
    finally:
        if 'connection' in locals():
            connection.close()

    return json.dumps(crimes)

@api.route('/help')
def get_help():
    return flask.render_template('help.html')

@api.route('/charts/crimesOverTime')
def crimes_over_time():
    '''
    Returns aggregated data for visualization based on selected filters
    '''
    start = request.args.get('start_month')
    end = request.args.get('end_month')
    areas = request.args.get('areas', '').split(',')
    types = request.args.get('types', '').split(',')

    # Validate required parameters
    if not all([start, end, areas[0], types[0]]):
        return json.dumps({
            "error": "Missing required parameters. Required: start_month, end_month, areas, types"
        }), 400

    # Validate date format
    if not (start.match(r'^\d{4}-\d{2}$') and end.match(r'^\d{4}-\d{2}$')):
        return json.dumps({
            "error": "Invalid date format. Use YYYY-MM"
        }), 400

    try:
        conn = get_connection()
        if not conn:
            return json.dumps({"error": "Database connection failed"}), 500

        cur = conn.cursor()

        # Convert areas and types to lowercase for case-insensitive comparison
        areas_lower = [area.lower() for area in areas if area]
        types_lower = [type_.lower() for type_ in types if type_]
        
        if not areas_lower or not types_lower:
            return json.dumps({
                "error": "At least one area and one type must be selected"
            }), 400

        # Create the array literals for the SQL query
        areas_array = "{" + ",".join(f'"{area}"' for area in areas_lower) + "}"
        types_array = "{" + ",".join(f'"{type_}"' for type_ in types_lower) + "}"

        query = '''
            SELECT months.month, crimes.vict_age, crimes.vict_sex
            FROM crimes
            JOIN crime_events ON crimes.id = crime_events.crime_id
            JOIN types ON types.id = crime_events.type_id
            JOIN months ON months.id = crime_events.month_id
            JOIN areas ON areas.id = crime_events.area_id
            WHERE months.month BETWEEN %s AND %s
            AND LOWER(areas.area) = ANY(%s)
            AND LOWER(types.type) = ANY(%s)
            ORDER BY months.month ASC;
        '''
        
        cur.execute(query, (start, end, areas_array, types_array))
        rows = cur.fetchall()

        if not rows:
            return json.dumps({"message": "No data found for the given criteria"}), 404

        # Initialize data structures for aggregation
        month_counts = {}
        age_buckets = {}
        sex_counts = {'M': 0, 'F': 0, 'X': 0}

        # Process the results
        for row in rows:
            month, age, sex = row
            
            # Count by month
            month_counts[month] = month_counts.get(month, 0) + 1
            
            # Count by age bucket
            if age and age > 0:
                bucket = f"{(age // 10) * 10}-{(age // 10) * 10 + 9}"
                age_buckets[bucket] = age_buckets.get(bucket, 0) + 1
            
            # Count by sex
            if sex in sex_counts:
                sex_counts[sex] += 1

        return json.dumps({
            "month_counts": month_counts,
            "age_buckets": age_buckets,
            "sex_counts": sex_counts
        })

    except Exception as e:
        print(f"Error generating chart data: {e}", file=sys.stderr)
        return json.dumps({"error": "Internal server error"}), 500
    finally:
        if 'conn' in locals():
            conn.close()

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
    '''
    Returns aggregated data for all charts based on selected filters:
    - Crimes by month counts
    - Age distribution in 10-year buckets
    - Gender distribution
    Filters include: date range, areas, and crime types
    '''
    start = request.args.get('start_month')
    end = request.args.get('end_month')
    areas = request.args.get('areas', '').split(',')
    types = request.args.get('types', '').split(',')

    # Initialize counts for all possible months
    counts_by_month = {
        "2024-06": 0, "2024-07": 0, "2024-08": 0,
        "2024-09": 0, "2024-10": 0, "2024-11": 0,
        "2024-12": 0, "2025-01": 0, "2025-02": 0,
        "2025-03": 0
    }
    age_buckets = {}
    sex_counts = {}

    try:
        conn = get_connection()
        cur = conn.cursor()

        # Convert areas and types to lowercase for case-insensitive comparison
        areas_lower = [area.lower() for area in areas if area]
        types_lower = [type_.lower() for type_ in types if type_]
        
        if not areas_lower or not types_lower:
            return json.dumps({
                "month_counts": counts_by_month,
                "age_buckets": {},
                "sex_counts": {}
            })

        # Create the array literals for the SQL query
        areas_array = "{" + ",".join(f'"{area}"' for area in areas_lower) + "}"
        types_array = "{" + ",".join(f'"{type_}"' for type_ in types_lower) + "}"

        query = '''
            SELECT months.month, crimes.vict_age, crimes.vict_sex
            FROM crimes
            JOIN crime_events ON crimes.id = crime_events.crime_id
            JOIN months ON crime_events.month_id = months.id
            JOIN areas ON crime_events.area_id = areas.id
            JOIN types ON crime_events.type_id = types.id
            WHERE (months.month >= %s OR %s IS NULL)
              AND (months.month <= %s OR %s IS NULL)
              AND LOWER(areas.area) = ANY(%s::text[])
              AND LOWER(types.type) = ANY(%s::text[])
        '''
        
        params = [start, start, end, end, areas_array, types_array]
        
        print(f"Executing query with params: {params}", file=sys.stderr)
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

        print(f"Found data: {counts_by_month}", file=sys.stderr)

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