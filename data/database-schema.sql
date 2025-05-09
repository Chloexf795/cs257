CREATE TABLE crimes (
    id SERIAL PRIMARY KEY,
    vict_age INTEGER,
    vict_sex TEXT,
    location TEXT
);

CREATE TABLE types (
    id integer NOT NULL,
    type TEXT
);

CREATE TABLE months (
    id SERIAL PRIMARY KEY,
    month TEXT
);

CREATE TABLE areas (
    id SERIAL PRIMARY KEY,
    area TEXT
);

CREATE TABLE crime_events (
    crime_id integer,
    type_id integer,
    month_id integer,
    area_id integer
);