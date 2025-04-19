#!/usr/bin/env python3

"""
NAME: cli.py
AUTHOR: Chloe Xufeng

SYNOPSIS:
    python3 cli.py crimesbyareaname AREANAME

DESCRIPTION:
    Shows a list of crimes reported in the specified AREA NAME (case-insensitive),
    based on the Crime Data from 2020 to Present dataset.
"""

import argparse
import csv

def crimes_by_area(area_name):
    data_file = "/Users/chloe/Downloads/CS 257/cs257/data/crime-data.csv"
    try:
        with open(data_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            print(f"Crimes in area: {area_name}\n")
            found = False
            for row in reader:
                if row['AREA NAME'].lower() == area_name.lower():
                    found = True
                    print(f"- {row['DATE OCC']}: {row['Crm Cd Desc']}")
            if not found:
                print("No records found for that area.")
    except FileNotFoundError:
        print("Data file not found. Please make sure the path is correct.")

def main():
    parser = argparse.ArgumentParser(description="Query crimes by area name.")
    subparsers = parser.add_subparsers(dest="command")

    area_parser = subparsers.add_parser("crimesbyareaname", help="Show all crimes in a given AREA NAME")
    area_parser.add_argument("areaname", type=str, help="The AREA NAME to search for (e.g., Wilshire)")

    args = parser.parse_args()

    if args.command == "crimesbyareaname":
        crimes_by_area(args.areaname)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
