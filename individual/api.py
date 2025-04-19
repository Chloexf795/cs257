#!/usr/bin/env python3
"""
api.py
Author: Chloe Xufeng
Date: 2025-04-16

Citation: Based on flask_sample.py provided in course materials.
"""

from flask import Flask, request, jsonify
import csv

app = Flask(__name__)

DATA_FILE = "../data/crime-data.csv"

# -- Endpoint 1: Main functionality --
@app.route("/crimesbyareaname")
def crimes_by_area():
    area = request.args.get("name", "")
    if not area:
        return jsonify({"error": "Missing 'name' parameter in query string"}), 400

    results = []
    try:
        with open(DATA_FILE, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            reader.fieldnames = [name.strip() for name in reader.fieldnames]  # clean headers
            for row in reader:
                if row['AREA NAME'].strip().lower() == area.lower():
                    results.append({
                        "date": row['DATE OCC'],
                        "description": row['Crm Cd Desc']
                    })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "area": area,
        "count": len(results),
        "crimes": results
    })


# -- Endpoint 2: Help endpoint --
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
    import sys
    if len(sys.argv) != 3:
        print("Usage: python3 api.py host port")
    else:
        host = sys.argv[1]
        port = int(sys.argv[2])
        app.run(host=host, port=port)
