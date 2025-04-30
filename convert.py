#!/usr/bin/env python3
"""
convert.py
Author: Chloe Xufeng, Owen Xu
Reads crimeData2025.csv and writes:
- crime_types.csv
- crime_times.csv
- locations.csv
- crimes.csv
"""

import csv
from datetime import datetime

# Input and output paths
INPUT_FILE = 'data/crimeData2025.csv'

def main():
    crime_types = {}
    crime_times = {}
    locations = {}

    crime_type_id = 0
    time_id = 0
    location_id = 0

    crimes = []

    with open(INPUT_FILE, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)  # Skip header row

        for row in reader:
            # Column positions based on file format
            date_occ = row[0]
            time_occ = row[1]
            area_name = row[2]
            crm_cd_desc = row[3]
            vict_age = row[4]
            vict_sex = row[5]
            location = row[6]
            lat = row[7]
            lon = row[8]

            # Handle crime_types
            if crm_cd_desc not in crime_types:
                crime_types[crm_cd_desc] = crime_type_id
                crime_type_id += 1
            ct_id = crime_types[crm_cd_desc]

            # Handle crime_times
            time_key = (date_occ, time_occ)
            if time_key not in crime_times:
                crime_times[time_key] = time_id
                time_id += 1
            t_id = crime_times[time_key]

            # Handle locations
            loc_key = (location, lat, lon)
            if loc_key not in locations:
                locations[loc_key] = location_id
                location_id += 1
            l_id = locations[loc_key]

            # Add to main crime table
            crimes.append([ct_id, t_id, area_name, vict_age, vict_sex, l_id])

    # Write files
    with open('data/crime_types.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'crm_cd_desc'])
        for desc, id in crime_types.items():
            writer.writerow([id, desc])

    with open('data/crime_times.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'date_occ', 'time_occ'])
        for (date, time), id in crime_times.items():
            writer.writerow([id, date, time])

    with open('data/locations.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'location', 'lat', 'lon'])
        for (loc, lat, lon), id in locations.items():
            writer.writerow([id, loc, lat, lon])

    with open('data/crimes.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['crime_type_id', 'time_id', 'area_name', 'vict_age', 'vict_sex', 'location_id'])
        for crime in crimes:
            writer.writerow(crime)

if __name__ == '__main__':
    main()
