# cs257
This is the Git repo used for CS 257 software design. 

Old - New database Pair: 
crime_types - types
crime_times - months
locations - areas
crimes - crimes
crimes_crime_types_crimes_times_locations - crime_events

# crime_types
id: Unique ID for the crime type
crm_cd_desc: Description of the crime (e.g., theft, arson)

# types
id: Unique ID for the crime type
type: type of the crime (e.g., theft, arson)

# crime_times
id: Unique ID for the time record
date_occ: Date of occurrence (format: MM-DD-YYYY 00:00:00)
time_occ: Time of occurrence (in 24-hour HHMM format)

# months
id: Unique ID for the month record
month: the year-month of occurrence (format: yyyy-mm)

# locations
id: Unique ID for the location
location: the district of the indicent
(followed will may be added later:
street: street-level address or block of incident 
lat: Latitude coordinate
lon: Longitude coordinate
)

# areas
id: Unique ID for the area
location: the district of the indicent

# crimes (Old)
id: Unique ID for the crime
vict_age: The age of the victim
vict_sex: The sex of the victim
premis_desc: Premise description, basically the type of location where the crime happened 

# crimes (New)
id: Unique ID for the crime
vict_age: The age of the victim
vict_sex: The sex of the victim
location: the type of location where the crime happened 

# crimes_crime_types_crimes_times_locations 
crime_id integer,
crime_type_id integer,
crime_time_id integer,
location_id integer

# crime_events
crime_id: Unique ID for the crime
type_id: Unique ID for the crime type
month_id: Unique ID for the month record
area_id: Unique ID for the location
