'''
CREATE TABLE crimes (
    id SERIAL PRIMARY KEY,
    crime_type_id INTEGER REFERENCES crime_types(id),
    time_id INTEGER REFERENCES crime_times(id),
    area_name TEXT,
    vict_age INTEGER,
    vict_sex TEXT,
    location_id INTEGER REFERENCES locations(id)
);
'''
CREATE TABLE crimes (
    id SERIAL PRIMARY KEY,
    vict_age INTEGER,
    vict_sex TEXT,
    premis_desc TEXT
);



CREATE TABLE crime_types (
    id SERIAL PRIMARY KEY,
    crm_cd_desc TEXT
);

CREATE TABLE crime_times (
    id SERIAL PRIMARY KEY,
    date_occ TIMESTAMP,
    time_occ INTEGER
);

CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    location TEXT,
    lat FLOAT,
    lon FLOAT
);

CREATE TABLE crimes_crime_types_crimes_times_locations (
    crime_id integer,
    crime_type_id integer,
    crime_time_id integer,
    location_id integer
);