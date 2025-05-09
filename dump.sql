--
-- PostgreSQL database dump
--

-- Dumped from database version 13.20
-- Dumped by pg_dump version 13.20

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE ONLY public.months DROP CONSTRAINT months_pkey;
ALTER TABLE ONLY public.crimes DROP CONSTRAINT crimes_pkey;
ALTER TABLE ONLY public.areas DROP CONSTRAINT areas_pkey;
ALTER TABLE public.months ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.crimes ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.areas ALTER COLUMN id DROP DEFAULT;
DROP TABLE public.types;
DROP SEQUENCE public.months_id_seq;
DROP TABLE public.months;
DROP SEQUENCE public.crimes_id_seq;
DROP TABLE public.crimes;
DROP TABLE public.crime_events;
DROP SEQUENCE public.areas_id_seq;
DROP TABLE public.areas;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: areas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.areas (
    id integer NOT NULL,
    area text
);


--
-- Name: areas_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.areas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: areas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.areas_id_seq OWNED BY public.areas.id;


--
-- Name: crime_events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crime_events (
    crime_id integer,
    type_id integer,
    month_id integer,
    area_id integer
);


--
-- Name: crimes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crimes (
    id integer NOT NULL,
    vict_age integer,
    vict_sex text,
    location text
);


--
-- Name: crimes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.crimes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: crimes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.crimes_id_seq OWNED BY public.crimes.id;


--
-- Name: months; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.months (
    id integer NOT NULL,
    month text
);


--
-- Name: months_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.months_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: months_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.months_id_seq OWNED BY public.months.id;


--
-- Name: types; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.types (
    id integer NOT NULL,
    type text
);


--
-- Name: areas id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.areas ALTER COLUMN id SET DEFAULT nextval('public.areas_id_seq'::regclass);


--
-- Name: crimes id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crimes ALTER COLUMN id SET DEFAULT nextval('public.crimes_id_seq'::regclass);


--
-- Name: months id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.months ALTER COLUMN id SET DEFAULT nextval('public.months_id_seq'::regclass);


--
-- Data for Name: areas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.areas (id, area) FROM stdin;
0	Topanga
1	Northeast
2	Harbor
3	Newton
4	Southwest
5	Southeast
6	West Valley
7	Mission
8	Devonshire
9	77th Street
10	Hollenbeck
11	Wilshire
12	Pacific
13	West LA
14	Foothill
15	Van Nuys
16	Central
17	Rampart
18	N Hollywood
19	Olympic
\.


--
-- Data for Name: crime_events; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crime_events (crime_id, type_id, month_id, area_id) FROM stdin;
0	0	0	0
1	1	1	1
2	2	2	2
2	3	2	2
2	4	1	2
3	5	1	3
2	6	1	4
4	7	1	5
2	6	0	4
5	2	0	2
6	1	2	6
7	8	0	7
8	0	1	8
9	4	0	2
2	2	0	4
10	9	0	9
2	2	1	4
5	2	2	10
5	2	0	2
2	3	1	10
11	5	1	3
12	1	1	2
2	6	0	4
13	10	0	3
2	6	2	4
14	5	2	11
15	2	0	12
2	4	1	2
2	6	1	4
2	6	1	4
16	11	0	7
2	4	1	2
17	8	1	1
2	2	2	2
18	12	1	5
19	9	1	13
2	2	2	2
2	6	0	4
20	0	1	7
2	3	2	11
21	13	2	1
2	2	0	4
15	2	0	12
2	3	2	11
2	4	0	2
22	14	1	8
23	15	1	1
24	4	0	2
25	13	1	9
26	4	1	10
26	13	1	13
2	2	2	4
27	0	1	5
28	16	2	2
29	17	0	3
30	0	1	14
2	4	1	2
31	2	1	2
26	10	2	8
2	2	1	4
32	18	1	2
2	6	1	4
2	2	0	2
33	11	1	2
34	5	0	7
2	6	0	4
35	15	0	1
2	2	2	4
18	8	2	5
6	19	2	6
18	11	0	10
36	13	1	2
9	4	0	2
20	7	1	7
37	9	0	2
38	11	2	8
2	4	1	2
39	20	1	6
2	2	1	10
40	4	2	7
37	0	1	15
9	4	0	2
15	2	1	4
41	4	1	7
42	4	2	7
2	4	1	2
2	6	2	4
16	8	2	7
43	4	1	4
9	4	0	2
24	21	1	0
17	19	1	14
2	4	1	2
44	22	0	1
45	2	1	4
16	4	1	8
2	2	2	4
17	19	1	1
46	23	1	1
47	0	1	2
48	2	1	4
6	19	1	6
2	2	0	4
2	2	1	4
49	21	0	16
5	2	0	9
9	4	0	2
0	0	1	8
2	4	0	2
50	0	0	2
2	4	1	4
51	24	1	7
16	8	2	13
52	8	0	7
2	6	0	4
2	4	0	2
48	2	0	4
2	4	0	2
2	6	1	4
16	11	1	8
2	4	0	2
24	1	2	0
53	2	1	4
54	15	1	14
2	4	1	2
2	6	1	4
55	0	0	10
2	2	1	12
2	6	2	4
40	4	2	6
5	2	2	4
18	12	1	5
56	4	0	4
57	2	1	4
58	13	2	0
59	10	1	6
5	4	0	2
60	13	2	0
6	25	0	6
61	20	1	7
19	9	1	10
9	4	0	2
2	6	1	4
62	7	1	7
16	4	0	8
2	2	1	2
2	3	1	3
2	6	0	4
63	9	1	7
2	2	0	9
5	2	0	2
64	2	0	4
2	6	1	4
2	6	2	2
65	26	1	1
11	27	2	8
2	4	1	2
2	4	2	2
65	0	2	10
2	4	1	2
66	13	2	0
67	9	2	6
68	1	1	16
16	4	0	8
2	4	1	2
69	0	2	7
70	5	2	12
47	28	0	2
2	2	1	4
19	0	0	15
2	4	0	2
12	1	1	5
2	6	0	4
27	5	2	9
2	6	1	4
9	4	0	2
71	0	1	8
12	1	0	9
72	12	0	14
63	27	2	8
2	2	2	2
69	0	2	6
6	20	1	6
4	29	2	7
2	2	1	4
2	2	2	4
17	0	1	1
73	13	0	17
18	13	0	13
74	0	0	13
2	2	0	4
75	13	2	10
2	6	0	4
5	6	1	12
76	0	1	8
77	4	0	7
21	0	1	8
78	7	1	18
18	4	0	13
2	4	0	2
79	1	2	0
2	2	2	4
2	2	1	4
2	2	1	4
2	6	2	4
2	4	1	2
76	9	0	18
2	4	1	2
5	2	2	2
2	4	0	2
2	4	0	2
2	4	0	2
26	23	1	5
1	1	1	19
80	10	1	14
2	6	0	4
2	6	1	4
5	2	0	4
69	0	2	6
2	6	1	4
2	2	1	4
21	4	2	3
81	4	1	7
5	2	0	12
2	6	2	4
2	2	2	4
69	0	0	8
43	2	1	4
82	0	0	1
9	4	0	2
2	6	1	4
2	2	1	4
83	5	2	10
11	5	2	10
19	9	0	1
84	0	2	5
11	13	2	8
2	2	1	4
85	17	0	8
2	2	1	14
5	6	0	4
26	11	2	10
18	23	0	5
76	0	0	8
27	30	2	7
18	8	1	5
24	10	0	3
5	4	1	2
76	9	1	7
2	2	0	4
53	6	1	4
86	11	0	2
2	2	2	2
2	4	1	2
5	6	1	4
69	31	0	8
9	4	0	2
9	4	0	2
2	4	1	2
87	21	1	0
88	0	1	8
2	6	1	4
5	2	1	2
2	4	1	2
5	2	0	4
2	2	1	4
61	20	1	7
2	6	1	4
2	6	0	4
2	23	2	2
2	6	1	4
26	10	1	5
2	2	0	12
79	1	1	0
89	21	1	10
2	4	0	2
26	11	1	5
90	6	0	4
91	2	1	4
2	6	1	4
92	17	0	3
93	32	0	4
2	4	1	2
94	26	0	6
19	0	0	8
37	30	2	7
64	2	1	4
95	23	2	2
38	4	0	0
2	2	1	4
5	6	1	4
22	5	0	2
2	2	1	14
96	17	2	7
\.


--
-- Data for Name: crimes; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.crimes (id, vict_age, vict_sex, location) FROM stdin;
0	12	F	JUNIOR HIGH SCHOOL
1	0	X	STREET
2	0		STREET
3	15	M	JUNIOR HIGH SCHOOL
4	16	F	SINGLE FAMILY DWELLING
5	0		PARKING LOT
6	0	M	PARK/PLAYGROUND
7	0	X	OTHER STORE
8	53	M	HIGH SCHOOL
9	0		SLIPS/DOCK/MARINA/BOAT
10	10	M	ELEMENTARY SCHOOL
11	16	M	STREET
12	0	X	POLICE FACILITY
13	42	M	OTHER BUSINESS
14	16	M	BUS STOP
15	0		GARAGE/CARPORT
16	0	X	HIGH SCHOOL
17	0	X	PARK/PLAYGROUND
18	0	X	ELEMENTARY SCHOOL
19	17	M	HIGH SCHOOL
20	17	F	STREET
21	14	F	HIGH SCHOOL
22	15	F	HIGH SCHOOL
23	32	M	PARK/PLAYGROUND
24	0	M	STREET
25	13	M	BUS STOP
26	0	X	JUNIOR HIGH SCHOOL
27	14	M	JUNIOR HIGH SCHOOL
28	32	F	PARKING LOT
29	13	F	JUNIOR HIGH SCHOOL
30	13	M	HIGH SCHOOL
31	0		OTHER PREMISE
32	13	F	MULTI-UNIT DWELLING (APARTMENT, DUPLEX, ETC)
33	51	M	STORAGE SHED
34	16	F	BUS STOP
35	30	F	PARKING LOT
36	54	M	JUNIOR HIGH SCHOOL
37	13	M	JUNIOR HIGH SCHOOL
38	0	M	JUNIOR HIGH SCHOOL
39	29	F	HIGH SCHOOL
40	0	M	ELEMENTARY SCHOOL
41	59	M	HIGH SCHOOL
42	15	M	HIGH SCHOOL
43	0		SIDEWALK
44	18	F	MULTI-UNIT DWELLING (APARTMENT, DUPLEX, ETC)
45	0		HOSPITAL
46	33	M	PARK/PLAYGROUND
47	15	F	STREET
48	0		MULTI-UNIT DWELLING (APARTMENT, DUPLEX, ETC)
49	4	F	HOSPITAL
50	13	F	PARK/PLAYGROUND
51	13	M	DRIVEWAY
52	0	F	ELEMENTARY SCHOOL
53	0		ELEMENTARY SCHOOL
54	40	M	STREET
55	18	M	HIGH SCHOOL
56	24	X	HIGH SCHOOL
57	0		BUS DEPOT/TERMINAL, OTHER THAN MTA
58	51	M	COLLEGE/JUNIOR COLLEGE/UNIVERSITY
59	0	M	HIGH SCHOOL
60	24	M	COLLEGE/JUNIOR COLLEGE/UNIVERSITY
61	36	M	JUNIOR HIGH SCHOOL
62	14	F	VEHICLE, PASSENGER/TRUCK
63	14	M	STREET
64	0		SINGLE FAMILY DWELLING
65	22	M	PARK/PLAYGROUND
66	35	M	SPECIALTY SCHOOL/OTHER
67	16	M	PARK/PLAYGROUND
68	0	M	DETENTION/JAIL FACILITY
69	16	M	HIGH SCHOOL
70	18	M	STREET
71	49	M	JUNIOR HIGH SCHOOL
72	29	M	PARK/PLAYGROUND
73	70	F	SINGLE FAMILY DWELLING
74	17	F	HIGH SCHOOL
75	11	M	HIGH SCHOOL
76	16	F	HIGH SCHOOL
77	36	M	ELEMENTARY SCHOOL
78	14	F	STREET
79	35	M	STREET
80	31	M	VEHICLE, PASSENGER/TRUCK
81	36	F	ELEMENTARY SCHOOL
82	25	F	PARK/PLAYGROUND
83	14	M	DRIVEWAY
84	17	F	MTA BUS
85	17	F	PARKING LOT
86	46	M	OTHER BUSINESS
87	4	F	STREET
88	67	F	JUNIOR HIGH SCHOOL
89	11	M	SINGLE FAMILY DWELLING
90	0		YARD (RESIDENTIAL/BUSINESS)
91	0		COLLEGE/JUNIOR COLLEGE/UNIVERSITY
92	16	F	STREET
93	24	X	OTHER BUSINESS
94	68	M	PARKING LOT
95	57	F	HIGH SCHOOL
96	35	F	HIGH SCHOOL
\.


--
-- Data for Name: months; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.months (id, month) FROM stdin;
0	2025-01
1	2025-02
2	2025-03
\.


--
-- Data for Name: types; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.types (id, type) FROM stdin;
0	BATTERY - SIMPLE ASSAULT
1	OTHER MISCELLANEOUS CRIME
2	VEHICLE - STOLEN
3	THEFT FROM MOTOR VEHICLE - PETTY ($950 & UNDER)
4	THEFT-GRAND ($950.01 & OVER)EXCPT,GUNS,FOWL,LIVESTK,PROD
5	ROBBERY
6	VEHICLE, STOLEN - OTHER (MOTORIZED SCOOTERS, BIKES, ETC)
7	CHILD ANNOYING (17YRS & UNDER)
8	VANDALISM - MISDEAMEANOR ($399 OR UNDER)
9	ASSAULT WITH DEADLY WEAPON, AGGRAVATED ASSAULT
10	VANDALISM - FELONY ($400 & OVER, ALL CHURCH VANDALISMS)
11	BURGLARY
12	ARSON
13	CRIMINAL THREATS - NO WEAPON DISPLAYED
14	SEX,UNLAWFUL(INC MUTUAL CONSENT, PENETRATION W/ FRGN OBJ
15	BURGLARY FROM VEHICLE
16	VEHICLE - ATTEMPT STOLEN
17	INDECENT EXPOSURE
18	RAPE, FORCIBLE
19	TRESPASSING
20	VIOLATION OF COURT ORDER
21	CHILD NEGLECT (SEE 300 W.I.C.)
22	THEFT OF IDENTITY
23	THEFT PLAIN - PETTY ($950 & UNDER)
24	EXTORTION
25	ILLEGAL DUMPING
26	THEFT FROM MOTOR VEHICLE - GRAND ($950.01 AND OVER)
27	BRANDISH WEAPON
28	BATTERY WITH SEXUAL CONTACT
29	CHILD PORNOGRAPHY
30	ASSAULT WITH DEADLY WEAPON ON POLICE OFFICER
31	THEFT FROM PERSON - ATTEMPT
32	SHOPLIFTING - PETTY THEFT ($950 & UNDER)
\.


--
-- Name: areas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.areas_id_seq', 1, false);


--
-- Name: crimes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crimes_id_seq', 1, false);


--
-- Name: months_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.months_id_seq', 1, false);


--
-- Name: areas areas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.areas
    ADD CONSTRAINT areas_pkey PRIMARY KEY (id);


--
-- Name: crimes crimes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crimes
    ADD CONSTRAINT crimes_pkey PRIMARY KEY (id);


--
-- Name: months months_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.months
    ADD CONSTRAINT months_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

