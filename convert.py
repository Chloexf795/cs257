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
INPUT_FILE = 'data/2024&2025data.csv'

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
            area = row[1]
            crm_cd_desc = row[2]
            vict_age = row[3]
            vict_sex = row[4]
            crime_type = convert_type(crm_cd_desc)

            # Handle crime_types
            if crime_type not in crime_types:
                crime_types[crime_type] = crime_type_id
                crime_type_id += 1
            ct_id = crime_types[crime_type]

            # Handle crime_times
            dt = datetime.strptime(date_occ, "%m/%d/%Y %I:%M:%S %p")
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
            
            crime_key = (vict_age, vict_sex)
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
            print(f'this is crime: {desc}')
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
        for (vict_age, vict_sex), id in crimes.items():
            writer.writerow([id, vict_age, vict_sex])

    with open('data/crime_events.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for ids in crimes_crime_types_crimes_times_areas:
            writer.writerow(ids)

def convert_type(crm_cd_desc):
    crime_categories = {
        "theft": [
            "VEHICLE - STOLEN",
            "VEHICLE, STOLEN - OTHER (MOTORIZED SCOOTERS, BIKES, ETC)",
            "THEFT FROM MOTOR VEHICLE - PETTY ($950 & UNDER)",
            "VEHICLE - ATTEMPT STOLEN",
            "THEFT-GRAND ($950.01 & OVER)EXCPT,GUNS,FOWL,LIVESTK,PROD",
            "THEFT OF IDENTITY",
            "THEFT PLAIN - PETTY ($950 & UNDER)",
            "THEFT FROM MOTOR VEHICLE - GRAND ($950.01 AND OVER)",
            "THEFT FROM PERSON - ATTEMPT",
            "SHOPLIFTING - PETTY THEFT ($950 & UNDER)",
            "SHOPLIFTING-GRAND THEFT ($950.01 & OVER)",
            "BIKE - STOLEN",
            "DEFRAUDING INNKEEPER/THEFT OF SERVICES, $950 & UNDER",
            "THEFT, PERSON",
            "DEFRAUDING INNKEEPER/THEFT OF SERVICES, OVER $950.01",
            "EMBEZZLEMENT, PETTY THEFT ($950 & UNDER)",
            "EMBEZZLEMENT, GRAND THEFT ($950.01 & OVER)"
        ],
        "vandalism": [
            "VANDALISM - MISDEAMEANOR ($399 OR UNDER)",
            "VANDALISM - FELONY ($400 & OVER, ALL CHURCH VANDALISMS)",
            "ARSON"
        ],
        "robbery": [
            "BURGLARY",
            "BURGLARY FROM VEHICLE",
            "SHOPLIFTING - ATTEMPT",
            "BURGLARY FROM VEHICLE, ATTEMPTED",
            "BURGLARY, ATTEMPTED",
            "ATTEMPTED ROBBERY",
            "ROBBERY"
        ],
        "assault": [
            "BATTERY - SIMPLE ASSAULT",
            "ASSAULT WITH DEADLY WEAPON, AGGRAVATED ASSAULT",
            "SEX,UNLAWFUL(INC MUTUAL CONSENT, PENETRATION W/ FRGN OBJ",
            "ASSAULT WITH DEADLY WEAPON ON POLICE OFFICER",
            "INTIMATE PARTNER - AGGRAVATED ASSAULT",
            "INTIMATE PARTNER - SIMPLE ASSAULT",
            "BATTERY POLICE (SIMPLE)",
            "OTHER ASSAULT"
        ],
        "sex crime": [
            "RAPE, FORCIBLE",
            "INDECENT EXPOSURE",
            "BATTERY WITH SEXUAL CONTACT",
            "LEWD CONDUCT",
            "ORAL COPULATION",
            "PIMPING"
        ],
        "criminal threats": [
            "CRIMINAL THREATS - NO WEAPON DISPLAYED",
            "BRANDISH WEAPON",
            "STALKING"
        ],
        "child crime": [
            "CHILD ANNOYING (17YRS & UNDER)",
            "CHILD NEGLECT (SEE 300 W.I.C.)",
            "CHILD PORNOGRAPHY"
        ],
        "other crime": [
            "OTHER MISCELLANEOUS CRIME",
            "TRESPASSING",
            "VIOLATION OF COURT ORDER",
            "EXTORTION",
            "ILLEGAL DUMPING",
            "DRIVING WITHOUT OWNER CONSENT (DWOC)",
            "LETTERS, LEWD  -  TELEPHONE CALLS, LEWD",
            "PICKPOCKET",
            "DISCHARGE FIREARMS/SHOTS FIRED",
            "DOCUMENT FORGERY / STOLEN FELONY",
            "FAILURE TO YIELD",
            "DRUNK ROLL",
            "CONTEMPT OF COURT",
            "FALSE IMPRISONMENT",
            "VIOLATION OF RESTRAINING ORDER",
            "RESISTING ARREST",
            "KIDNAPPING",
            "FALSE POLICE REPORT"
        ]
    }
    for category, crimes in crime_categories.items():
        if crm_cd_desc in crimes:
            return category
    return crm_cd_desc

if __name__ == '__main__':
    main()
