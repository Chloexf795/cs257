SELECT crime_types.crm_cd
FROM crime_types;

SELECT locations.location
FROM locations;

SELECT crime_times.time_occ
FROM crime_times;

SELECT crimes.vict_age, crimes.vict_sex, crimes.
FROM crimes, locations, crime_types, dates
WHERE crime_types = 'VEHICLE - STOLEN'
AND locations = 'Central'
AND dates = '02/21/2025'
AND crimes.id = crimes_crime_types_crimes_times_locations.crime_id
AND crime_types.id = crimes_crime_types_crimes_times_locations.crime_type_id
AND locations.id = crimes_crime_types_crimes_times_locations.location_id
AND crime_id = crimes_crime_types_crimes_times_locations.crime_time_id;

