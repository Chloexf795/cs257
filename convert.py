#!/usr/bin/env python3
"""
convert.py
Author: Chloe Xufeng, Owen Xu
Converts refined crimeData2025.csv into normalized CSVs:
- crime_types.csv
- crime_times.csv
- locations.csv
- crimes.csv
"""

import csv
from datetime import datetime

INPUT_FILE = 'data/crimeData2025.csv'

# Helper to clean values
def clean(value):
    return str(value).strip() if value and str(value).strip() else '\\N'

def main():
    crime_types = {}
    crime_times = {}
    locations = {}

    crime_type_id = 1
    time_id = 1
    location_id = 1

    crime_types_rows = []
    crime_times_rows = []
    locations_rows = []
    crimes_rows = []
\