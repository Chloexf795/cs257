#!/usr/bin/env python3
"""
convert.py
Author: Chloe Xufeng, Owen Xu
Reads crimeData2025.csv and writes:
- crime_types.csv
- crime_times.csv
- areas.csv
- crimes.csv
"""

import csv
from datetime import datetime

# Input and output paths
INPUT_FILE = 'data/crimeData2025.csv'

def main():
    crime_types = {}
    crime_times = {}
    areas = {}
    crimes = {}
    crime_type_id = 0
    time_id = 0
    area_id = 0
    crime_id = 0
    crimes_crime_types_crimes_times_areas = []

    with open(INPUT_FILE, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)  # Skip header row

        for row in reader:
            # Column positions based on file format
            date_occ = row[0]
            time_occ = row[1]
            area = row[2]
            crm_cd_desc = row[3]
            vict_age = row[4]
            vict_sex = row[5]
            '''
            location = row[6]
            lat = row[7]
            lon = row[8]
            '''
            premis_desc = row[9]

            # Handle crime_types
            if crm_cd_desc not in crime_types:
                crime_types[crm_cd_desc] = crime_type_id
                crime_type_id += 1
            ct_id = crime_types[crm_cd_desc]

            # Handle crime_times
            time_key = (date_occ, time_occ)
            dt = datetime.strptime(time_key[0], "%m/%d/%Y %I:%M:%S %p")
            year_month = dt.strftime("%Y-%m")
            if year_month not in crime_times:
                crime_times[year_month] = time_id
                time_id += 1
            t_id = crime_times[year_month]

            # Handle locations
            #loc_key = (location, lat, lon)
            if area not in areas:
                areas[area] = area_id
                area_id += 1
            a_id = areas[area]
            
            crime_key = (vict_age, vict_sex, premis_desc)
            if crime_key not in crimes:
                crimes[crime_key] = crime_id
                crime_id += 1
            c_id = crimes[crime_key]
            

            # Add to main crime table
            crimes_crime_types_crimes_times_areas.append([c_id, ct_id, t_id, a_id])

    # Write files
    with open('data/crime_types.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for desc, id in crime_types.items():
            writer.writerow([id, desc])

    with open('data/crime_times.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for (year_month), id in crime_times.items():
            writer.writerow([id, year_month])

    with open('data/areas.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        '''
        for (loc, lat, lon), id in locations.items():
            writer.writerow([id, loc, lat, lon])
        '''
        for (area, id) in areas.items():
            writer.writerow([id, area])

    with open('data/crimes.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for (vict_age, vict_sex, premis_desc), id in crimes.items():
            writer.writerow([id, vict_age, vict_sex, premis_desc])

    with open('data/crimes_crime_types_crimes_times_locations.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for ids in crimes_crime_types_crimes_times_areas:
            writer.writerow(ids)

if __name__ == '__main__':
    main()
