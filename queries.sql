/*
Old version:

SELECT crime_types.crm_cd_desc     
FROM crime_types;

SELECT locations.location
FROM locations;

SELECT crime_times.time_occ
FROM crime_times;

SELECT crimes.vict_age, crimes.vict_sex, crimes.premis_desc 
FROM crimes, locations, crime_types, crime_times, crimes_crime_types_crimes_times_locations
WHERE crime_types.crm_cd_desc = 'BATTERY - SIMPLE ASSAULT'
AND locations.location = 'Topanga'
AND crime_times.date_occ = '01/14/2025 00:00:00'
AND crimes.id = crimes_crime_types_crimes_times_locations.crime_id
AND crime_types.id = crimes_crime_types_crimes_times_locations.crime_type_id
AND locations.id = crimes_crime_types_crimes_times_locations.location_id
AND crime_times.id = crimes_crime_types_crimes_times_locations.crime_time_id;

*/

SELECT types.type     
FROM types;

SELECT areas.area
FROM areas;

SELECT months.month
FROM months;

SELECT crimes.vict_age, crimes.vict_sex, crimes.location 
FROM crimes, areas, types, months, crime_events
WHERE types.type = 'BATTERY - SIMPLE ASSAULT'
AND areas.area = 'Topanga'
AND months.month = '2025-01'
AND crimes.id = crime_events.crime_id
AND types.id = crime_events.type_id
AND areas.id = crime_events.area_id
AND months.id = crime_events.month_id;
