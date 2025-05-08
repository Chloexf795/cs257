CREATE TABLE crimes (
    id SERIAL PRIMARY KEY,
    vict_age INTEGER,
    vict_sex TEXT,
    premis_desc TEXT
);



CREATE TABLE crime_types (
    id integer NOT NULL,
    crm_cd_desc TEXT
);

CREATE TABLE crime_times (
    id SERIAL PRIMARY KEY,
    date_occ TEXT
);

CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    location TEXT
);

CREATE TABLE crimes_crime_types_crimes_times_locations (
    crime_id integer,
    crime_type_id integer,
    crime_time_id integer,
    location_id integer
);