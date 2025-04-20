#!/usr/bin/env python3
"""
api.py
Author: Chloe Xufeng
Date: 2025-04-16

Citation: Based on flask_sample.py provided in course materials.
"""

import flask
import csv
import json
import argparse

app = flask.Flask(__name__)

DATA_FILE = "../data/crime-data.csv"

# -- Root --
@app.route('/')
def index():
    return 'This is Crime API. Try /help or /crimesbyareaname?name=Central'

# -- Endpoint 1: Main functionality --
@app.route("/crimesbyareaname")
def crimes_by_area():
    area = flask.request.args.get("name", "")
    if not area:
        return json.dumps({"error": "Missing 'name' parameter in query string"}), 400, {'Content-Type': 'application/json'}

    results = []
    try:
        with open(DATA_FILE, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            reader.fieldnames = [name.strip() for name in reader.fieldnames]
            for row in reader:
                if row['AREA NAME'].strip().lower() == area.lower():
                    results.append({
                        "date": row['DATE OCC'],
                        "description": row['Crm Cd Desc']
                    })
    except Exception as e:
        return json.dumps({"error": str(e)}), 500, {'Content-Type': 'application/json'}

    response = {
        "area": area,
        "count": len(results),
        "crimes": results
    }
    return json.dumps(response), 200, {'Content-Type': 'application/json'}

# -- Endpoint 2: Help --
@app.route("/help")
def help():
    return """
    <h1>Crime API Documentation</h1>
    <h2>/crimesbyareaname</h2>
    <p><strong>Request:</strong> GET /crimesbyareaname?name=AREA_NAME</p>
    <p><strong>Response:</strong> JSON list of crimes in that AREA NAME</p>
    <pre>
    {
        "area": "Central",
        "count": 3,
        "crimes": [
            {
                "date": "03/01/2020",
                "description": "VEHICLE - STOLEN"
            },
            ...
        ]
    }
    </pre>
    """

# -- Run the app --
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crime API Server")
    parser.add_argument("host", help="Host to run the server on (e.g. localhost)")
    parser.add_argument("port", type=int, help="Port to run the server on (e.g. 9999)")
    args = parser.parse_args()

    app.run(host=args.host, port=args.port, debug=True)
