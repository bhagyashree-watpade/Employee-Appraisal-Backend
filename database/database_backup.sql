--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: appraisal_cycle; Type: TABLE; Schema: public; Owner: pg_database_owner
--

CREATE TABLE public.appraisal_cycle (
    cycle_id integer NOT NULL,
    cycle_name character varying(100) NOT NULL,
    description text NOT NULL,
    status character varying(20),
    start_date_of_cycle date NOT NULL,
    end_date_of_cycle date NOT NULL,
    CONSTRAINT appraisal_cycle_status_check CHECK (((status)::text = ANY ((ARRAY['active'::character varying, 'inactive'::character varying])::text[])))
);


ALTER TABLE public.appraisal_cycle OWNER TO pg_database_owner;

--
-- Name: appraisal_cycle_cycle_id_seq; Type: SEQUENCE; Schema: public; Owner: pg_database_owner
--

CREATE SEQUENCE public.appraisal_cycle_cycle_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.appraisal_cycle_cycle_id_seq OWNER TO pg_database_owner;

--
-- Name: appraisal_cycle_cycle_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pg_database_owner
--

ALTER SEQUENCE public.appraisal_cycle_cycle_id_seq OWNED BY public.appraisal_cycle.cycle_id;


--
-- Name: employee; Type: TABLE; Schema: public; Owner: pg_database_owner
--

CREATE TABLE public.employee (
    employee_id integer NOT NULL,
    employee_name character varying(100) NOT NULL,
    role character varying(50),
    reporting_manager integer,
    previous_reporting_manager integer,
    password character varying(10) NOT NULL
);


ALTER TABLE public.employee OWNER TO pg_database_owner;

--
-- Name: employee_allocation; Type: TABLE; Schema: public; Owner: pg_database_owner
--

CREATE TABLE public.employee_allocation (
    allocation_id integer NOT NULL,
    cycle_id integer,
    employee_id integer
);


ALTER TABLE public.employee_allocation OWNER TO pg_database_owner;

--
-- Name: employee_allocation_allocation_id_seq; Type: SEQUENCE; Schema: public; Owner: pg_database_owner
--

CREATE SEQUENCE public.employee_allocation_allocation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.employee_allocation_allocation_id_seq OWNER TO pg_database_owner;

--
-- Name: employee_allocation_allocation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pg_database_owner
--

ALTER SEQUENCE public.employee_allocation_allocation_id_seq OWNED BY public.employee_allocation.allocation_id;


--
-- Name: employee_employee_id_seq; Type: SEQUENCE; Schema: public; Owner: pg_database_owner
--

CREATE SEQUENCE public.employee_employee_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.employee_employee_id_seq OWNER TO pg_database_owner;

--
-- Name: employee_employee_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pg_database_owner
--

ALTER SEQUENCE public.employee_employee_id_seq OWNED BY public.employee.employee_id;


--
-- Name: lead_assessment_rating; Type: TABLE; Schema: public; Owner: pg_database_owner
--

CREATE TABLE public.lead_assessment_rating (
    lead_rating_id integer NOT NULL,
    allocation_id integer,
    cycle_id integer,
    employee_id integer,
    parameter_id integer,
    parameter_rating integer,
    specific_input text,
    CONSTRAINT lead_assessment_rating_parameter_rating_check CHECK (((parameter_rating >= 1) AND (parameter_rating <= 4)))
);


ALTER TABLE public.lead_assessment_rating OWNER TO pg_database_owner;

--
-- Name: lead_assessment_rating_lead_rating_id_seq; Type: SEQUENCE; Schema: public; Owner: pg_database_owner
--

CREATE SEQUENCE public.lead_assessment_rating_lead_rating_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.lead_assessment_rating_lead_rating_id_seq OWNER TO pg_database_owner;

--
-- Name: lead_assessment_rating_lead_rating_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pg_database_owner
--

ALTER SEQUENCE public.lead_assessment_rating_lead_rating_id_seq OWNED BY public.lead_assessment_rating.lead_rating_id;


--
-- Name: option; Type: TABLE; Schema: public; Owner: pg_database_owner
--

CREATE TABLE public.option (
    option_id integer NOT NULL,
    question_id integer,
    option_text text NOT NULL
);


ALTER TABLE public.option OWNER TO pg_database_owner;

--
-- Name: option_option_id_seq; Type: SEQUENCE; Schema: public; Owner: pg_database_owner
--

CREATE SEQUENCE public.option_option_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.option_option_id_seq OWNER TO pg_database_owner;

--
-- Name: option_option_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pg_database_owner
--

ALTER SEQUENCE public.option_option_id_seq OWNED BY public.option.option_id;


--
-- Name: parameters; Type: TABLE; Schema: public; Owner: pg_database_owner
--

CREATE TABLE public.parameters (
    parameter_id integer NOT NULL,
    parameter_title character varying(255) NOT NULL,
    helptext text,
    cycle_id integer,
    applicable_to_employee boolean,
    applicable_to_lead boolean,
    is_fixed_parameter boolean
);


ALTER TABLE public.parameters OWNER TO pg_database_owner;

--
-- Name: parameters_parameter_id_seq; Type: SEQUENCE; Schema: public; Owner: pg_database_owner
--

CREATE SEQUENCE public.parameters_parameter_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.parameters_parameter_id_seq OWNER TO pg_database_owner;

--
-- Name: parameters_parameter_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pg_database_owner
--

ALTER SEQUENCE public.parameters_parameter_id_seq OWNED BY public.parameters.parameter_id;


--
-- Name: question; Type: TABLE; Schema: public; Owner: pg_database_owner
--

CREATE TABLE public.question (
    question_id integer NOT NULL,
    question_type character varying(50),
    question_text text NOT NULL
);


ALTER TABLE public.question OWNER TO pg_database_owner;

--
-- Name: question_question_id_seq; Type: SEQUENCE; Schema: public; Owner: pg_database_owner
--

CREATE SEQUENCE public.question_question_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.question_question_id_seq OWNER TO pg_database_owner;

--
-- Name: question_question_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pg_database_owner
--

ALTER SEQUENCE public.question_question_id_seq OWNED BY public.question.question_id;


--
-- Name: self_assessment_response; Type: TABLE; Schema: public; Owner: pg_database_owner
--

CREATE TABLE public.self_assessment_response (
    response_id integer NOT NULL,
    allocation_id integer,
    cycle_id integer,
    employee_id integer,
    question_id integer,
    option_id integer,
    response_text text
);


ALTER TABLE public.self_assessment_response OWNER TO pg_database_owner;

--
-- Name: self_assessment_response_response_id_seq; Type: SEQUENCE; Schema: public; Owner: pg_database_owner
--

CREATE SEQUENCE public.self_assessment_response_response_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.self_assessment_response_response_id_seq OWNER TO pg_database_owner;

--
-- Name: self_assessment_response_response_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pg_database_owner
--

ALTER SEQUENCE public.self_assessment_response_response_id_seq OWNED BY public.self_assessment_response.response_id;


--
-- Name: stages; Type: TABLE; Schema: public; Owner: pg_database_owner
--

CREATE TABLE public.stages (
    stage_id integer NOT NULL,
    stage_name character varying(50) NOT NULL,
    cycle_id integer,
    start_date_of_stage date NOT NULL,
    end_date_of_stage date NOT NULL
);


ALTER TABLE public.stages OWNER TO pg_database_owner;

--
-- Name: stages_stage_id_seq; Type: SEQUENCE; Schema: public; Owner: pg_database_owner
--

CREATE SEQUENCE public.stages_stage_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.stages_stage_id_seq OWNER TO pg_database_owner;

--
-- Name: stages_stage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pg_database_owner
--

ALTER SEQUENCE public.stages_stage_id_seq OWNED BY public.stages.stage_id;


--
-- Name: appraisal_cycle cycle_id; Type: DEFAULT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.appraisal_cycle ALTER COLUMN cycle_id SET DEFAULT nextval('public.appraisal_cycle_cycle_id_seq'::regclass);


--
-- Name: employee employee_id; Type: DEFAULT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.employee ALTER COLUMN employee_id SET DEFAULT nextval('public.employee_employee_id_seq'::regclass);


--
-- Name: employee_allocation allocation_id; Type: DEFAULT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.employee_allocation ALTER COLUMN allocation_id SET DEFAULT nextval('public.employee_allocation_allocation_id_seq'::regclass);


--
-- Name: lead_assessment_rating lead_rating_id; Type: DEFAULT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.lead_assessment_rating ALTER COLUMN lead_rating_id SET DEFAULT nextval('public.lead_assessment_rating_lead_rating_id_seq'::regclass);


--
-- Name: option option_id; Type: DEFAULT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.option ALTER COLUMN option_id SET DEFAULT nextval('public.option_option_id_seq'::regclass);


--
-- Name: parameters parameter_id; Type: DEFAULT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.parameters ALTER COLUMN parameter_id SET DEFAULT nextval('public.parameters_parameter_id_seq'::regclass);


--
-- Name: question question_id; Type: DEFAULT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.question ALTER COLUMN question_id SET DEFAULT nextval('public.question_question_id_seq'::regclass);


--
-- Name: self_assessment_response response_id; Type: DEFAULT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.self_assessment_response ALTER COLUMN response_id SET DEFAULT nextval('public.self_assessment_response_response_id_seq'::regclass);


--
-- Name: stages stage_id; Type: DEFAULT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.stages ALTER COLUMN stage_id SET DEFAULT nextval('public.stages_stage_id_seq'::regclass);


--
-- Data for Name: appraisal_cycle; Type: TABLE DATA; Schema: public; Owner: pg_database_owner
--

COPY public.appraisal_cycle (cycle_id, cycle_name, description, status, start_date_of_cycle, end_date_of_cycle) FROM stdin;
1	Annual Performance Review	Yearly evaluation of employee performance.	active	2024-01-01	2024-12-31
2	Mid-Year Performance Review	Half-yearly appraisal to track progress.	active	2024-07-01	2024-12-31
3	Quarterly Performance Review - Q1	First quarter performance evaluation.	inactive	2024-01-01	2024-03-31
4	Quarterly Performance Review - Q2	Second quarter performance evaluation.	active	2024-04-01	2024-06-30
5	Demo11	ksfksdjkfdsklfjdsklfjs	active	2025-03-01	2025-08-28
6	Demo23	ksfksdjkfdsklfjdsklfjs	active	2025-03-01	2025-08-28
7	Demo23	ksfksdjkfdsklfjdsklfjs	active	2025-03-01	2025-08-28
8	Demo23	ksfksdjkfdsklfjdsklfjs	active	2025-03-01	2025-08-28
\.


--
-- Data for Name: employee; Type: TABLE DATA; Schema: public; Owner: pg_database_owner
--

COPY public.employee (employee_id, employee_name, role, reporting_manager, previous_reporting_manager, password) FROM stdin;
1	Virat Kohli	Team Lead	4	4	1234
2	Rohit Sharma	Employee	1	1	1234
3	Jasprit Bumrah	Employee	5	1	1234
4	MS Dhoni	HR	\N	\N	1234
5	Sachin Tendulkar	Team Lead	4	4	1234
\.


--
-- Data for Name: employee_allocation; Type: TABLE DATA; Schema: public; Owner: pg_database_owner
--

COPY public.employee_allocation (allocation_id, cycle_id, employee_id) FROM stdin;
\.


--
-- Data for Name: lead_assessment_rating; Type: TABLE DATA; Schema: public; Owner: pg_database_owner
--

COPY public.lead_assessment_rating (lead_rating_id, allocation_id, cycle_id, employee_id, parameter_id, parameter_rating, specific_input) FROM stdin;
\.


--
-- Data for Name: option; Type: TABLE DATA; Schema: public; Owner: pg_database_owner
--

COPY public.option (option_id, question_id, option_text) FROM stdin;
1	1	Python
2	1	HTML
3	1	C++
4	1	Photoshop
5	2	Tokyo
6	2	Beijing
7	2	Seoul
8	2	Bangkok
9	3	True
10	3	False
11	4	True
12	4	False
13	7	A Python framework
14	7	A database
15	7	A front-end library
16	8	Parth
17	8	Fab
18	8	Sham
19	9	parth
20	10	Good 
21	10	Not Good
22	13	Always
23	13	Most of the times
24	13	Occasionally
25	13	Rarely
26	15	Pune
27	15	Nashik
28	15	Kolhapur
29	15	Ratnagiri
30	21	Demo1
31	21	Demo2
32	22	Hello
33	22	How
34	23	Yes
35	23	No
36	24	Lol
37	24	Haha
38	24	Ohhh
39	25	Kolhapur
40	25	Ratnagiri
41	27	Yes
42	27	No
43	28	lsdkfjs
44	30	kdkd
45	31	Yes
46	31	No
47	32	kfdj
48	36	sdfsfs
49	37	Yes
50	37	No
51	40	No
52	41	dsfsdf
53	42	dsfsdfdsf11
54	43	fsdfsdsd22
55	44	e33
56	45	No
57	51	sdfsd
\.


--
-- Data for Name: parameters; Type: TABLE DATA; Schema: public; Owner: pg_database_owner
--

COPY public.parameters (parameter_id, parameter_title, helptext, cycle_id, applicable_to_employee, applicable_to_lead, is_fixed_parameter) FROM stdin;
1	Job Knowledge	Understanding of job roles and responsibilities.	1	t	t	f
2	Communication Skills	Ability to effectively communicate within the team and with stakeholders.	1	t	t	f
3	Team Collaboration	Effectiveness in working with colleagues and contributing to team goals.	1	t	t	f
4	Overall Performance Rating	Overall performance	1	t	t	t
5	Innovation	Initiative in bringing new ideas and improvements.	2	t	f	f
6	Leadership Potential	Ability to take ownership and guide teams effectively.	2	f	t	f
7	Overall Performance Rating	Overall performance	2	t	t	t
8	Customer Focus	Ability to understand and meet customer expectations.	3	t	t	f
9	Problem-Solving	Skill in identifying and resolving work-related challenges.	3	t	t	f
10	Overall Performance Rating	Overall performance	3	t	t	t
11	Time Management	Effectiveness in prioritizing and completing tasks on time.	4	t	f	f
12	Decision Making	Ability to make well-informed, effective, and timely decisions.	4	f	t	f
13	Overall Performance Rating	Overall performance	4	t	t	t
14	Overall Performance Rating	dksjdfks	5	t	t	t
15			5	f	f	f
16	Overall Performance Rating	dksjdfks	6	t	t	t
17			6	f	f	f
18			6	f	f	f
19			6	f	f	f
20	Overall Performance Rating	dksjdfks	7	t	t	t
21			7	f	f	f
22			7	f	f	f
23			7	f	f	f
24			7	f	f	f
25	Overall Performance Rating	dksjdfks	8	t	t	t
26			8	f	f	f
27			8	f	f	f
28			8	f	f	f
29			8	f	f	f
30			8	f	f	f
\.


--
-- Data for Name: question; Type: TABLE DATA; Schema: public; Owner: pg_database_owner
--

COPY public.question (question_id, question_type, question_text) FROM stdin;
1	MCQ	Which of the following are programming languages?
2	Single choice	What is the capital of Japan?
3	True/false	The sun rises in the east.
4	True/false	Penguins can fly.
5	Descriptive	List down your strengths and weaknesses
6	MCQ	What is FastAPI?
7	MCQ	What is FastAPI?
8	MCQ	What is your name?
9	MCQ	Hello parth
10	MCQ	How are you?
11	Descriptive	What's a skill you'd love to learn, and why?
12	Yes/No	You're going to the party, aren't you?
13	MCQ	How often have you met your assigned deadlines?
14	Yes/No	Do you like Python programming language?
15	MCQ	Where do you live?
16	Yes/No	Do you like live in pune?
17	Yes/No	Do you like sports?
18	Yes/No	Do like cars?
19	Yes/No	Demo question 1
20	Yes/No	Demo Question 2
21	MCQ	Demo Question 3
22	Yes/No	Demo Question 4
23	Yes/No	Demo Question 5
24	MCQ	Demo Question 6
25	MCQ	Demo Question 22
26	MCQ	How often have you met your assigned deadlines?
27	Yes/No	How often have you met your assigned deadlines?
28	MCQ	How are you?
29	MCQ	How are you?
30	MCQ	Demo2222
31	Yes/No	ldskfjsdk
32	MCQ	How are you?
33	Descriptive	Hello parth
34	Rating_Scale	Demo Question sdlfkjs
35	Descriptive	kdfjsksjdf
36	MCQ	sdfsdfsd
37	Yes/No	werwerew
38	Single_Choice	werwer
39	MCQ	sdfdsfsf
40	Yes/No	Demo 24
41	MCQ	How are you?
42	MCQ	How often have you met your assigned deadlines?
43	MCQ	fgdfgfdgdf22
44	MCQ	e33
45	Yes/No	How often have you met your assigned deadlines?
46	Single_Choice	How often have you met your assigned deadlines?
47	Single_Choice	How often have you met your assigned deadlines?
48	Descriptive	Demo9
49	Single_Choice	Demo9
50	Descriptive	Demo 50 Qustion
51	MCQ	dfgfdf
52	Descriptive	lskdfjlskdfj
53	Descriptive	sfjsdk
54	Descriptive	sdfsdf
\.


--
-- Data for Name: self_assessment_response; Type: TABLE DATA; Schema: public; Owner: pg_database_owner
--

COPY public.self_assessment_response (response_id, allocation_id, cycle_id, employee_id, question_id, option_id, response_text) FROM stdin;
\.


--
-- Data for Name: stages; Type: TABLE DATA; Schema: public; Owner: pg_database_owner
--

COPY public.stages (stage_id, stage_name, cycle_id, start_date_of_stage, end_date_of_stage) FROM stdin;
1	Setup	1	2024-01-05	2024-01-10
2	Self Assessment	1	2024-02-01	2024-02-10
3	Lead Assessment	1	2024-03-01	2024-03-10
4	HR/VL Validation	1	2024-04-01	2024-04-07
5	Closure	1	2024-05-01	2024-05-05
6	Setup	2	2024-07-05	2024-07-10
7	Self Assessment	2	2024-08-01	2024-08-07
8	Lead Assessment	2	2024-09-01	2024-09-07
9	HR/VL Validation	2	2024-10-01	2024-10-05
10	Closure	2	2024-11-01	2024-11-05
11	Setup	3	2024-01-02	2024-01-05
12	Self Assessment	3	2024-01-10	2024-01-15
13	Lead Assessment	3	2024-02-01	2024-02-05
14	HR/VL Validation	3	2024-02-20	2024-02-25
15	Closure	3	2024-03-10	2024-03-15
16	Setup	4	2024-04-02	2024-04-05
17	Self Assessment	4	2024-04-10	2024-04-15
18	Lead Assessment	4	2024-05-01	2024-05-05
19	HR/VL Validation	4	2024-05-20	2024-05-25
20	Closure	4	2024-06-15	2024-06-20
21	Setup	5	2025-03-01	2025-03-28
22	Self Assessment	5	2025-03-29	2025-04-28
23	Lead Assessment	5	2025-05-01	2025-05-10
24	HR/VL Validation	5	2025-05-11	2025-05-15
25	Closure	5	2025-05-28	2025-06-28
26	Setup	6	2025-03-01	2025-03-28
27	Self Assessment	6	2025-03-29	2025-04-28
28	Lead Assessment	6	2025-05-01	2025-05-10
29	HR/VL Validation	6	2025-05-11	2025-05-15
30	Closure	6	2025-05-28	2025-06-28
31	Setup	7	2025-03-01	2025-03-28
32	Self Assessment	7	2025-03-29	2025-04-28
33	Lead Assessment	7	2025-05-01	2025-05-10
34	HR/VL Validation	7	2025-05-11	2025-05-15
35	Closure	7	2025-05-28	2025-06-28
36	Setup	8	2025-03-01	2025-03-28
37	Self Assessment	8	2025-03-29	2025-04-28
38	Lead Assessment	8	2025-05-01	2025-05-10
39	HR/VL Validation	8	2025-05-11	2025-05-15
40	Closure	8	2025-05-28	2025-06-28
\.


--
-- Name: appraisal_cycle_cycle_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pg_database_owner
--

SELECT pg_catalog.setval('public.appraisal_cycle_cycle_id_seq', 12, true);


--
-- Name: employee_allocation_allocation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pg_database_owner
--

SELECT pg_catalog.setval('public.employee_allocation_allocation_id_seq', 1, false);


--
-- Name: employee_employee_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pg_database_owner
--

SELECT pg_catalog.setval('public.employee_employee_id_seq', 5, true);


--
-- Name: lead_assessment_rating_lead_rating_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pg_database_owner
--

SELECT pg_catalog.setval('public.lead_assessment_rating_lead_rating_id_seq', 1, false);


--
-- Name: option_option_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pg_database_owner
--

SELECT pg_catalog.setval('public.option_option_id_seq', 57, true);


--
-- Name: parameters_parameter_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pg_database_owner
--

SELECT pg_catalog.setval('public.parameters_parameter_id_seq', 37, true);


--
-- Name: question_question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pg_database_owner
--

SELECT pg_catalog.setval('public.question_question_id_seq', 54, true);


--
-- Name: self_assessment_response_response_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pg_database_owner
--

SELECT pg_catalog.setval('public.self_assessment_response_response_id_seq', 1, false);


--
-- Name: stages_stage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pg_database_owner
--

SELECT pg_catalog.setval('public.stages_stage_id_seq', 60, true);


--
-- Name: appraisal_cycle appraisal_cycle_pkey; Type: CONSTRAINT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.appraisal_cycle
    ADD CONSTRAINT appraisal_cycle_pkey PRIMARY KEY (cycle_id);


--
-- Name: employee_allocation employee_allocation_pkey; Type: CONSTRAINT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.employee_allocation
    ADD CONSTRAINT employee_allocation_pkey PRIMARY KEY (allocation_id);


--
-- Name: employee employee_pkey; Type: CONSTRAINT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_pkey PRIMARY KEY (employee_id);


--
-- Name: lead_assessment_rating lead_assessment_rating_pkey; Type: CONSTRAINT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.lead_assessment_rating
    ADD CONSTRAINT lead_assessment_rating_pkey PRIMARY KEY (lead_rating_id);


--
-- Name: option option_pkey; Type: CONSTRAINT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.option
    ADD CONSTRAINT option_pkey PRIMARY KEY (option_id);


--
-- Name: parameters parameters_pkey; Type: CONSTRAINT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.parameters
    ADD CONSTRAINT parameters_pkey PRIMARY KEY (parameter_id);


--
-- Name: question question_pkey; Type: CONSTRAINT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT question_pkey PRIMARY KEY (question_id);


--
-- Name: self_assessment_response self_assessment_response_pkey; Type: CONSTRAINT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.self_assessment_response
    ADD CONSTRAINT self_assessment_response_pkey PRIMARY KEY (response_id);


--
-- Name: stages stages_pkey; Type: CONSTRAINT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.stages
    ADD CONSTRAINT stages_pkey PRIMARY KEY (stage_id);


--
-- Name: employee_allocation employee_allocation_cycle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.employee_allocation
    ADD CONSTRAINT employee_allocation_cycle_id_fkey FOREIGN KEY (cycle_id) REFERENCES public.appraisal_cycle(cycle_id) ON DELETE CASCADE;


--
-- Name: employee_allocation employee_allocation_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.employee_allocation
    ADD CONSTRAINT employee_allocation_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employee(employee_id) ON DELETE CASCADE;


--
-- Name: employee employee_previous_reporting_manager_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_previous_reporting_manager_fkey FOREIGN KEY (previous_reporting_manager) REFERENCES public.employee(employee_id) ON DELETE SET NULL;


--
-- Name: employee employee_reporting_manager_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_reporting_manager_fkey FOREIGN KEY (reporting_manager) REFERENCES public.employee(employee_id) ON DELETE SET NULL;


--
-- Name: lead_assessment_rating lead_assessment_rating_allocation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.lead_assessment_rating
    ADD CONSTRAINT lead_assessment_rating_allocation_id_fkey FOREIGN KEY (allocation_id) REFERENCES public.employee_allocation(allocation_id) ON DELETE CASCADE;


--
-- Name: lead_assessment_rating lead_assessment_rating_cycle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.lead_assessment_rating
    ADD CONSTRAINT lead_assessment_rating_cycle_id_fkey FOREIGN KEY (cycle_id) REFERENCES public.appraisal_cycle(cycle_id) ON DELETE CASCADE;


--
-- Name: lead_assessment_rating lead_assessment_rating_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.lead_assessment_rating
    ADD CONSTRAINT lead_assessment_rating_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employee(employee_id) ON DELETE CASCADE;


--
-- Name: lead_assessment_rating lead_assessment_rating_parameter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.lead_assessment_rating
    ADD CONSTRAINT lead_assessment_rating_parameter_id_fkey FOREIGN KEY (parameter_id) REFERENCES public.parameters(parameter_id) ON DELETE CASCADE;


--
-- Name: option option_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.option
    ADD CONSTRAINT option_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.question(question_id) ON DELETE CASCADE;


--
-- Name: parameters parameters_cycle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.parameters
    ADD CONSTRAINT parameters_cycle_id_fkey FOREIGN KEY (cycle_id) REFERENCES public.appraisal_cycle(cycle_id) ON DELETE CASCADE;


--
-- Name: self_assessment_response self_assessment_response_allocation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.self_assessment_response
    ADD CONSTRAINT self_assessment_response_allocation_id_fkey FOREIGN KEY (allocation_id) REFERENCES public.employee_allocation(allocation_id) ON DELETE CASCADE;


--
-- Name: self_assessment_response self_assessment_response_cycle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.self_assessment_response
    ADD CONSTRAINT self_assessment_response_cycle_id_fkey FOREIGN KEY (cycle_id) REFERENCES public.appraisal_cycle(cycle_id) ON DELETE CASCADE;


--
-- Name: self_assessment_response self_assessment_response_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.self_assessment_response
    ADD CONSTRAINT self_assessment_response_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employee(employee_id) ON DELETE CASCADE;


--
-- Name: self_assessment_response self_assessment_response_option_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.self_assessment_response
    ADD CONSTRAINT self_assessment_response_option_id_fkey FOREIGN KEY (option_id) REFERENCES public.option(option_id) ON DELETE CASCADE;


--
-- Name: self_assessment_response self_assessment_response_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.self_assessment_response
    ADD CONSTRAINT self_assessment_response_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.question(question_id) ON DELETE CASCADE;


--
-- Name: stages stages_cycle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pg_database_owner
--

ALTER TABLE ONLY public.stages
    ADD CONSTRAINT stages_cycle_id_fkey FOREIGN KEY (cycle_id) REFERENCES public.appraisal_cycle(cycle_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

