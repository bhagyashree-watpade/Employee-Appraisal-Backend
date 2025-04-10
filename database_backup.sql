--
-- PostgreSQL database dump
--

-- Dumped from database version 11.22
-- Dumped by pg_dump version 11.22

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

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: appraisal_cycle; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.appraisal_cycle (
    cycle_id integer NOT NULL,
    cycle_name character varying(100) NOT NULL,
    description text NOT NULL,
    status character varying(20) NOT NULL,
    start_date_of_cycle date NOT NULL,
    end_date_of_cycle date NOT NULL,
    CONSTRAINT check_status CHECK (((status)::text = ANY ((ARRAY['active'::character varying, 'inactive'::character varying, 'completed'::character varying])::text[]))),
    CONSTRAINT status CHECK (((status)::text = ANY ((ARRAY['active'::character varying, 'inactive'::character varying, 'completed'::character varying])::text[])))
);


ALTER TABLE public.appraisal_cycle OWNER TO postgres;

--
-- Name: appraisal_cycle_cycle_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.appraisal_cycle_cycle_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.appraisal_cycle_cycle_id_seq OWNER TO postgres;

--
-- Name: appraisal_cycle_cycle_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.appraisal_cycle_cycle_id_seq OWNED BY public.appraisal_cycle.cycle_id;


--
-- Name: assigned_questions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.assigned_questions (
    assignment_id integer NOT NULL,
    cycle_id integer NOT NULL,
    employee_id integer NOT NULL,
    question_id integer NOT NULL
);


ALTER TABLE public.assigned_questions OWNER TO postgres;

--
-- Name: assigned_questions_assignment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.assigned_questions_assignment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.assigned_questions_assignment_id_seq OWNER TO postgres;

--
-- Name: assigned_questions_assignment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.assigned_questions_assignment_id_seq OWNED BY public.assigned_questions.assignment_id;


--
-- Name: employee; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employee (
    employee_id integer NOT NULL,
    employee_name character varying(100) NOT NULL,
    role character varying(50) NOT NULL,
    reporting_manager integer,
    previous_reporting_manager integer,
    password character varying(10) NOT NULL
);


ALTER TABLE public.employee OWNER TO postgres;

--
-- Name: employee_allocation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employee_allocation (
    allocation_id integer NOT NULL,
    cycle_id integer NOT NULL,
    employee_id integer NOT NULL
);


ALTER TABLE public.employee_allocation OWNER TO postgres;

--
-- Name: employee_allocation_allocation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.employee_allocation_allocation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.employee_allocation_allocation_id_seq OWNER TO postgres;

--
-- Name: employee_allocation_allocation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.employee_allocation_allocation_id_seq OWNED BY public.employee_allocation.allocation_id;


--
-- Name: employee_employee_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.employee_employee_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.employee_employee_id_seq OWNER TO postgres;

--
-- Name: employee_employee_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.employee_employee_id_seq OWNED BY public.employee.employee_id;


--
-- Name: lead_assessment_rating; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.lead_assessment_rating (
    lead_rating_id integer NOT NULL,
    allocation_id integer,
    cycle_id integer,
    employee_id integer,
    parameter_id integer,
    parameter_rating integer NOT NULL,
    specific_input text,
    discussion_date date NOT NULL,
    CONSTRAINT lead_assessment_rating_parameter_rating_check CHECK (((parameter_rating >= 1) AND (parameter_rating <= 4)))
);


ALTER TABLE public.lead_assessment_rating OWNER TO postgres;

--
-- Name: lead_assessment_rating_lead_rating_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.lead_assessment_rating_lead_rating_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.lead_assessment_rating_lead_rating_id_seq OWNER TO postgres;

--
-- Name: lead_assessment_rating_lead_rating_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.lead_assessment_rating_lead_rating_id_seq OWNED BY public.lead_assessment_rating.lead_rating_id;


--
-- Name: option; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.option (
    option_id integer NOT NULL,
    question_id integer,
    option_text text NOT NULL
);


ALTER TABLE public.option OWNER TO postgres;

--
-- Name: option_option_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.option_option_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.option_option_id_seq OWNER TO postgres;

--
-- Name: option_option_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.option_option_id_seq OWNED BY public.option.option_id;


--
-- Name: parameters; Type: TABLE; Schema: public; Owner: postgres
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


ALTER TABLE public.parameters OWNER TO postgres;

--
-- Name: parameters_parameter_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.parameters_parameter_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.parameters_parameter_id_seq OWNER TO postgres;

--
-- Name: parameters_parameter_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.parameters_parameter_id_seq OWNED BY public.parameters.parameter_id;


--
-- Name: question; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.question (
    question_id integer NOT NULL,
    question_type character varying(50),
    question_text text NOT NULL
);


ALTER TABLE public.question OWNER TO postgres;

--
-- Name: question_question_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.question_question_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.question_question_id_seq OWNER TO postgres;

--
-- Name: question_question_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.question_question_id_seq OWNED BY public.question.question_id;


--
-- Name: self_assessment_response; Type: TABLE; Schema: public; Owner: postgres
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


ALTER TABLE public.self_assessment_response OWNER TO postgres;

--
-- Name: self_assessment_response_response_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.self_assessment_response_response_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.self_assessment_response_response_id_seq OWNER TO postgres;

--
-- Name: self_assessment_response_response_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.self_assessment_response_response_id_seq OWNED BY public.self_assessment_response.response_id;


--
-- Name: stages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stages (
    stage_id integer NOT NULL,
    stage_name character varying(50) NOT NULL,
    cycle_id integer,
    start_date_of_stage date,
    end_date_of_stage date
);


ALTER TABLE public.stages OWNER TO postgres;

--
-- Name: stages_stage_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.stages_stage_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.stages_stage_id_seq OWNER TO postgres;

--
-- Name: stages_stage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.stages_stage_id_seq OWNED BY public.stages.stage_id;


--
-- Name: appraisal_cycle cycle_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appraisal_cycle ALTER COLUMN cycle_id SET DEFAULT nextval('public.appraisal_cycle_cycle_id_seq'::regclass);


--
-- Name: assigned_questions assignment_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assigned_questions ALTER COLUMN assignment_id SET DEFAULT nextval('public.assigned_questions_assignment_id_seq'::regclass);


--
-- Name: employee employee_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee ALTER COLUMN employee_id SET DEFAULT nextval('public.employee_employee_id_seq'::regclass);


--
-- Name: employee_allocation allocation_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee_allocation ALTER COLUMN allocation_id SET DEFAULT nextval('public.employee_allocation_allocation_id_seq'::regclass);


--
-- Name: lead_assessment_rating lead_rating_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lead_assessment_rating ALTER COLUMN lead_rating_id SET DEFAULT nextval('public.lead_assessment_rating_lead_rating_id_seq'::regclass);


--
-- Name: option option_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.option ALTER COLUMN option_id SET DEFAULT nextval('public.option_option_id_seq'::regclass);


--
-- Name: parameters parameter_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parameters ALTER COLUMN parameter_id SET DEFAULT nextval('public.parameters_parameter_id_seq'::regclass);


--
-- Name: question question_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question ALTER COLUMN question_id SET DEFAULT nextval('public.question_question_id_seq'::regclass);


--
-- Name: self_assessment_response response_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.self_assessment_response ALTER COLUMN response_id SET DEFAULT nextval('public.self_assessment_response_response_id_seq'::regclass);


--
-- Name: stages stage_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stages ALTER COLUMN stage_id SET DEFAULT nextval('public.stages_stage_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
4452b1eceb9c
\.


--
-- Data for Name: appraisal_cycle; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.appraisal_cycle (cycle_id, cycle_name, description, status, start_date_of_cycle, end_date_of_cycle) FROM stdin;
2	Mid-Year Performance Review	Half-yearly appraisal to track progress.	active	2024-07-01	2024-12-31
3	Quarterly Performance Review - Q1	First quarter performance evaluation.	inactive	2024-01-01	2024-03-31
4	Quarterly Performance Review - Q2	Second quarter performance evaluation.	active	2024-04-01	2024-06-30
15	Annual	ZXZx	active	2025-03-01	2025-03-30
16	Annual	ZXZx	active	2025-03-01	2025-03-30
21	annual	anualll	active	2025-03-01	2025-03-30
32	cycle 1	cycle	inactive	2025-03-01	2025-03-31
1	Annual Performance Review	Yearly evaluation of employee performance.	active	2024-01-01	2024-12-31
48	Annual Review 2023	End of year performance review for 2023	completed	2023-01-01	2023-12-31
49	Q1 2024 Appraisal	Quarterly appraisal for Q1 2024	completed	2024-01-01	2024-03-31
51	2024 Mid-Year Review	Mid-year performance appraisal cycle	active	2024-06-01	2024-06-30
52	2023 Year-End Review	Year-end performance appraisal	completed	2023-12-01	2023-12-31
53	2025 Q1 Review	Quarterly review for Q1 2025	inactive	2025-03-01	2025-03-31
54	cycle for demo	demo	inactive	2025-04-05	2025-04-30
55	string	string	active	2025-04-03	2025-04-03
56	app cycle 3	cycle 3	active	2025-04-01	2025-04-30
\.


--
-- Data for Name: assigned_questions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.assigned_questions (assignment_id, cycle_id, employee_id, question_id) FROM stdin;
1	1	2	2
2	1	2	4
3	1	2	5
4	1	2	7
5	1	2	10
6	1	3	2
7	1	3	4
8	1	3	5
9	1	3	7
10	1	3	10
11	1	5	2
12	1	5	4
13	1	5	5
14	1	5	7
15	1	5	10
16	1	10	2
17	1	10	4
18	1	10	5
19	1	10	7
20	1	10	10
22	2	1	1
23	2	1	3
24	2	2	1
25	2	2	3
26	2	3	1
27	2	3	3
28	3	2	3
29	3	2	4
31	2	16	2
\.


--
-- Data for Name: employee; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.employee (employee_id, employee_name, role, reporting_manager, previous_reporting_manager, password) FROM stdin;
1	Virat Kohli	Team Lead	4	4	1234
2	Rohit Sharma	Employee	1	1	1234
3	Jasprit Bumrah	Employee	5	1	1234
4	MS Dhoni	HR	\N	\N	1234
5	Sachin Tendulkar	Team Lead	4	4	1234
6	Shah Rukh Khan	Manager	\N	\N	pass1234
7	Amitabh Bachchan	Senior Manager	\N	\N	bigbpass
8	Salman Khan	Lead	2	\N	bhaipass1
9	Akshay Kumar	Lead	2	\N	khiladip
10	Hrithik Roshan	Employee	3	\N	hrithik11
11	Ranbir Kapoor	Employee	3	\N	ranbir22
12	Rajinikanth	Senior Manager	\N	\N	superstar
13	Kamal Haasan	Lead	7	\N	ulaganay
14	Vijay	Employee	8	\N	thalapathy
15	Allu Arjun	Employee	8	\N	pushpa123
16	Rahi	Employee	5	5	1234
\.


--
-- Data for Name: employee_allocation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.employee_allocation (allocation_id, cycle_id, employee_id) FROM stdin;
11	1	1
21	1	2
22	1	3
23	2	1
24	2	4
25	3	2
26	3	5
27	4	3
28	4	4
29	4	5
30	2	3
63	51	3
64	51	2
65	51	10
66	51	11
67	48	3
68	52	3
69	1	5
70	1	10
71	2	2
72	2	16
\.


--
-- Data for Name: lead_assessment_rating; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.lead_assessment_rating (lead_rating_id, allocation_id, cycle_id, employee_id, parameter_id, parameter_rating, specific_input, discussion_date) FROM stdin;
1	22	1	3	1	1	fjweliufwelirfh	2025-04-03
2	22	1	3	2	3	fjweliufwelirfh	2025-04-03
3	22	1	3	3	1	fjweliufwelirfh	2025-04-03
4	22	1	3	4	2	fjweliufwelirfh	2025-04-03
5	22	1	3	1	1	fjweliufwelirfh	2025-04-04
6	22	1	3	2	4	fjweliufwelirfh	2025-04-04
7	22	1	3	3	1	fjweliufwelirfh	2025-04-04
8	22	1	3	4	2	fjweliufwelirfh	2025-04-04
9	22	1	3	1	1	ui	2025-04-01
10	22	1	3	2	2	ui	2025-04-01
11	22	1	3	3	2	ui	2025-04-01
12	22	1	3	4	2	ui	2025-04-01
13	22	1	3	1	1		2025-04-01
14	22	1	3	2	2		2025-04-01
15	22	1	3	3	2		2025-04-01
16	22	1	3	4	2		2025-04-01
17	22	1	3	1	1		2025-04-02
18	22	1	3	2	1		2025-04-02
19	22	1	3	3	2		2025-04-02
20	22	1	3	4	2		2025-04-02
21	22	1	3	1	1		2025-04-01
22	22	1	3	2	2		2025-04-01
23	22	1	3	3	2		2025-04-01
24	22	1	3	4	3		2025-04-01
25	22	1	3	1	1		2025-04-01
26	22	1	3	2	2		2025-04-01
27	22	1	3	3	2		2025-04-01
28	22	1	3	4	3		2025-04-01
29	27	4	3	11	1		2025-04-09
30	27	4	3	13	2		2025-04-09
31	22	1	3	1	1		2025-04-01
32	22	1	3	2	2		2025-04-01
33	22	1	3	3	2		2025-04-01
34	22	1	3	4	3		2025-04-01
35	30	2	3	5	2		2025-04-02
36	30	2	3	7	2		2025-04-02
68	22	1	3	1	1	gooood	2025-04-04
69	22	1	3	2	2	gooood	2025-04-04
70	22	1	3	3	2	gooood	2025-04-04
71	22	1	3	4	2	gooood	2025-04-04
72	30	2	3	5	1		2025-04-02
73	30	2	3	7	2		2025-04-02
78	63	51	3	1	3	Good communication skills.	2024-03-10
79	64	51	2	2	4	Excellent problem-solving skills.	2024-03-12
80	65	51	10	3	3	Effective leadership.	2024-03-15
81	66	51	11	4	4	Outstanding performance.	2024-03-20
82	22	1	3	1	1		2025-04-04
83	22	1	3	2	2		2025-04-04
84	22	1	3	3	2		2025-04-04
85	22	1	3	4	2		2025-04-04
86	63	51	3	1	3	Good communication skills.	2024-03-10
87	64	51	3	2	4	Excellent problem-solving skills.	2024-03-12
88	65	51	3	3	3	Effective leadership.	2024-03-15
89	66	51	3	4	4	Outstanding performance.	2024-03-20
90	67	48	3	1	3	Good communication skills.	2024-03-10
91	67	48	3	2	4	Excellent problem-solving skills.	2024-03-12
92	67	48	3	3	3	Effective leadership.	2024-03-15
93	67	48	3	4	4	Outstanding performance.	2024-03-20
94	67	48	3	1	3	Good communication skills.	2024-03-10
95	67	48	3	2	4	Excellent problem-solving skills.	2024-03-12
96	67	48	3	3	3	Effective leadership.	2024-03-15
97	67	48	3	4	4	Outstanding performance.	2024-03-20
98	67	52	3	1	3	Good communication skills.	2024-03-10
99	67	52	3	2	4	Excellent problem-solving skills.	2024-03-12
100	67	52	3	3	3	Effective leadership.	2024-03-15
101	67	52	3	4	4	Outstanding performance.	2024-03-20
102	68	52	3	1	3	Good communication skills.	2024-03-10
103	68	52	3	2	4	Excellent problem-solving skills.	2024-03-12
104	68	52	3	3	3	Effective leadership.	2024-03-15
105	68	52	3	4	4	Outstanding performance.	2024-03-20
106	68	52	3	86	3	Good communication skills.	2024-03-10
107	68	52	3	87	4	Excellent problem-solving skills.	2024-03-12
108	68	52	3	88	3	Effective leadership.	2024-03-15
109	68	52	3	89	4	Outstanding performance.	2024-03-20
110	30	2	3	5	2	oasiaosd	2025-04-02
111	30	2	3	7	2	oasiaosd	2025-04-02
112	30	2	3	5	3	oasiaosd	2025-04-02
113	30	2	3	7	2	oasiaosd	2025-04-02
114	30	2	3	5	3	oasiaosd	2025-04-02
115	30	2	3	7	2	oasiaosd	2025-04-02
116	30	2	3	5	4	oasiaosd	2025-04-02
117	30	2	3	7	2	oasiaosd	2025-04-02
118	30	2	3	5	4	oasiaosd	2025-04-02
119	30	2	3	7	2	oasiaosd	2025-04-02
120	63	51	3	1	3	Good communication skills.	2024-03-10
121	63	51	3	2	4	Good communication skills.	2024-03-10
122	63	51	3	3	3	Good communication skills.	2024-03-10
123	63	51	3	4	4	Good communication skills.	2024-03-10
124	63	51	3	78	2	Good communication skills.	2024-03-10
125	63	51	3	79	1	Good communication skills.	2024-03-10
126	63	51	3	81	3	Good communication skills.	2024-03-10
127	30	2	3	5	4	oasiaosd	2025-04-02
128	30	2	3	7	2	oasiaosd	2025-04-02
129	30	2	3	5	4	oasiaosd	2025-04-02
130	30	2	3	7	2	oasiaosd	2025-04-02
131	30	2	3	5	1	uuuu	2025-04-02
132	30	2	3	7	2	uuuu	2025-04-02
133	30	2	3	5	1	uuuu	2025-04-02
134	30	2	3	7	2	uuuu	2025-04-02
135	72	2	16	5	2	pppp	2025-04-09
136	72	2	16	7	2	pppp	2025-04-09
137	72	2	16	5	1	ppppoooo	2025-04-09
138	72	2	16	7	1	ppppoooo	2025-04-09
139	30	2	3	5	1	uuuu	2025-04-07
140	30	2	3	7	2	uuuu	2025-04-07
141	72	2	16	5	1	ppppoooo	2025-04-09
142	72	2	16	7	1	ppppoooo	2025-04-09
143	72	2	16	5	2	good	2025-04-09
144	72	2	16	7	3	good	2025-04-09
\.


--
-- Data for Name: option; Type: TABLE DATA; Schema: public; Owner: postgres
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
13	6	Yes
14	6	No
15	7	Yes
16	7	No
17	8	a
18	8	ar
19	9	Yes
20	9	No
21	10	kekk
22	10	wkkek
23	12	Yes
24	12	No
25	13	Yes
26	13	No
27	15	i
28	15	j
29	17	Yes
30	17	No
31	20	Yes
32	20	No
33	21	Yes
34	21	No
35	22	Yes
36	22	No
37	23	sjhdhsjd
38	23	jashdjshd
39	24	jhj
40	24	hjh
41	26	Yes
42	26	No
43	27	Yes
44	27	No
45	28	Yes
46	28	No
\.


--
-- Data for Name: parameters; Type: TABLE DATA; Schema: public; Owner: postgres
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
78	Communication Skills	Ability to communicate effectively.	51	t	t	t
79	Problem Solving	Ability to resolve issues effectively.	51	t	t	t
80	Leadership	Ability to lead and guide a team.	51	f	t	t
81	Overall Performance Rating	Final overall rating.	51	t	t	t
82	Communication Skills	Ability to communicate effectively.	48	t	t	t
19	Overall Performance Rating		15	t	t	t
20	zcxmnx		15	t	f	f
21	Overall Performance Rating		16	t	t	t
22	zcxmnx		16	t	f	f
29	Overall Performance Rating		21	t	t	t
30	coding	coding style	21	t	f	f
54	Overall Performance Rating		32	t	t	t
55	hahhh	jajsj	32	t	f	f
56	ooooo	shhhha	32	t	t	f
57	tttt	jasjjjaj	32	f	t	f
58			32	t	t	f
83	Problem Solving	Ability to resolve issues effectively.	48	t	t	t
84	Leadership	Ability to lead and guide a team.	48	f	t	t
85	Overall Performance Rating	Final overall rating.	48	t	t	t
86	Communication Skills	Ability to communicate effectively.	52	t	t	t
87	Problem Solving	Ability to resolve issues effectively.	52	t	t	t
88	Leadership	Ability to lead and guide a team.	52	f	t	t
89	Overall Performance Rating	Final overall rating.	52	t	t	t
90	Overall Performance Rating		54	t	t	t
91	cummunication		54	t	f	f
92	coding style	ioooa	54	t	t	f
93	Overall Performance Rating		56	t	t	t
94	coding 	coding style	56	t	t	f
95	performance		56	t	f	f
\.


--
-- Data for Name: question; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.question (question_id, question_type, question_text) FROM stdin;
1	MCQ	Which of the following are programming languages?
2	Single choice	What is the capital of Japan?
3	True/false	The sun rises in the east.
4	True/false	Penguins can fly.
5	Descriptive	List down your strengths and weaknesses
6	Yes/No	shshajsh
7	Yes/No	sdmsnd,msdn
8	MCQ	ioooo
9	Yes/No	ouiiia
10	MCQ	sdkjadsk
11	MCQ	asmmmd
12	Yes/No	sdasd
13	Yes/No	uuu
14	Descriptive	jjjjj
15	MCQ	jjjj
16	Single_Choice	ooo
17	Yes/No	uuuopp
18	Descriptive	pppp
19	Descriptive	piuuu
20	Yes/No	oppppshjASDJ
21	Yes/No	Penguins can fly.
22	Yes/No	Penguins can fly.
23	MCQ	jsadakjsh
24	Yes/No	dwni
25	Descriptive	asdasd
26	Yes/No	fgf
27	Yes/No	asdasd
28	Yes/No	terter
\.


--
-- Data for Name: self_assessment_response; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.self_assessment_response (response_id, allocation_id, cycle_id, employee_id, question_id, option_id, response_text) FROM stdin;
\.


--
-- Data for Name: stages; Type: TABLE DATA; Schema: public; Owner: postgres
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
173	Setup	54	2025-04-05	2025-04-05
175	Lead Assessment	54	2025-04-07	2025-04-07
176	HR/VL Validation	54	2025-04-08	2025-04-09
178	Setup	56	2025-04-01	2025-04-02
179	Self Assessment	56	2025-04-03	2025-04-04
180	Lead Assessment	56	2025-04-05	2025-04-06
181	HR/VL Validation	56	2025-04-07	2025-04-08
182	Closure	56	2025-04-10	2025-04-11
38	Setup	15	2025-03-27	2025-03-29
39	Self Assessment	15	2025-03-01	2025-03-27
40	Lead Assessment	15	2025-03-20	2025-03-21
41	HR/VL validation	15	2025-03-23	2025-03-28
42	Closure	15	2025-03-20	2025-03-30
43	Setup	16	2025-03-27	2025-03-29
44	Self Assessment	16	2025-03-01	2025-03-27
45	Lead Assessment	16	2025-03-20	2025-03-21
46	HR/VL validation	16	2025-03-23	2025-03-28
47	Closure	16	2025-03-20	2025-03-30
63	Setup	21	2025-03-02	2025-03-09
64	Self Assessment	21	2025-03-04	2025-03-07
65	Lead Assessment	21	2025-03-11	2025-03-20
66	HR/VL Validation	21	2025-03-21	2025-03-27
67	Closure	21	2025-03-27	2025-03-29
118	Setup	32	2025-03-01	2025-03-02
119	Self Assessment	32	2025-03-08	2025-03-09
120	Lead Assessment	32	2025-03-10	2025-03-11
121	HR/VL Validation	32	2025-03-12	2025-03-14
122	Closure	32	2025-03-15	2025-03-18
174	Self Assessment	54	2025-04-06	2025-04-06
177	Closure	54	2025-04-14	2025-04-18
163	Setup	1	2024-05-25	2024-05-31
164	Self Assessment	1	2024-06-01	2024-06-05
165	Lead Assessment	1	2024-06-06	2024-06-15
166	HR/VL Validation	1	2024-06-16	2024-06-25
167	Closure	1	2024-06-26	2024-06-30
168	Setup	51	2024-05-25	2024-05-31
169	Self Assessment	51	2024-06-01	2024-06-05
170	Lead Assessment	51	2024-06-06	2024-06-15
171	HR/VL Validation	51	2024-06-16	2024-06-25
172	Closure	51	2024-06-26	2024-06-30
\.


--
-- Name: appraisal_cycle_cycle_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.appraisal_cycle_cycle_id_seq', 56, true);


--
-- Name: assigned_questions_assignment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.assigned_questions_assignment_id_seq', 31, true);


--
-- Name: employee_allocation_allocation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.employee_allocation_allocation_id_seq', 72, true);


--
-- Name: employee_employee_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.employee_employee_id_seq', 16, true);


--
-- Name: lead_assessment_rating_lead_rating_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.lead_assessment_rating_lead_rating_id_seq', 144, true);


--
-- Name: option_option_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.option_option_id_seq', 46, true);


--
-- Name: parameters_parameter_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.parameters_parameter_id_seq', 95, true);


--
-- Name: question_question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.question_question_id_seq', 28, true);


--
-- Name: self_assessment_response_response_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.self_assessment_response_response_id_seq', 1, false);


--
-- Name: stages_stage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.stages_stage_id_seq', 182, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: appraisal_cycle appraisal_cycle_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appraisal_cycle
    ADD CONSTRAINT appraisal_cycle_pkey PRIMARY KEY (cycle_id);


--
-- Name: assigned_questions assigned_questions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assigned_questions
    ADD CONSTRAINT assigned_questions_pkey PRIMARY KEY (assignment_id);


--
-- Name: employee_allocation employee_allocation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee_allocation
    ADD CONSTRAINT employee_allocation_pkey PRIMARY KEY (allocation_id);


--
-- Name: employee employee_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_pkey PRIMARY KEY (employee_id);


--
-- Name: lead_assessment_rating lead_assessment_rating_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lead_assessment_rating
    ADD CONSTRAINT lead_assessment_rating_pkey PRIMARY KEY (lead_rating_id);


--
-- Name: option option_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.option
    ADD CONSTRAINT option_pkey PRIMARY KEY (option_id);


--
-- Name: parameters parameters_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parameters
    ADD CONSTRAINT parameters_pkey PRIMARY KEY (parameter_id);


--
-- Name: question question_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT question_pkey PRIMARY KEY (question_id);


--
-- Name: self_assessment_response self_assessment_response_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.self_assessment_response
    ADD CONSTRAINT self_assessment_response_pkey PRIMARY KEY (response_id);


--
-- Name: stages stages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stages
    ADD CONSTRAINT stages_pkey PRIMARY KEY (stage_id);


--
-- Name: ix_employee_employee_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_employee_employee_id ON public.employee USING btree (employee_id);


--
-- Name: ix_lead_assessment_rating_lead_rating_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_lead_assessment_rating_lead_rating_id ON public.lead_assessment_rating USING btree (lead_rating_id);


--
-- Name: assigned_questions assigned_questions_cycle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assigned_questions
    ADD CONSTRAINT assigned_questions_cycle_id_fkey FOREIGN KEY (cycle_id) REFERENCES public.appraisal_cycle(cycle_id) ON DELETE CASCADE;


--
-- Name: assigned_questions assigned_questions_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assigned_questions
    ADD CONSTRAINT assigned_questions_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employee(employee_id) ON DELETE CASCADE;


--
-- Name: assigned_questions assigned_questions_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assigned_questions
    ADD CONSTRAINT assigned_questions_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.question(question_id) ON DELETE CASCADE;


--
-- Name: employee_allocation employee_allocation_cycle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee_allocation
    ADD CONSTRAINT employee_allocation_cycle_id_fkey FOREIGN KEY (cycle_id) REFERENCES public.appraisal_cycle(cycle_id) ON DELETE CASCADE;


--
-- Name: employee_allocation employee_allocation_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee_allocation
    ADD CONSTRAINT employee_allocation_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employee(employee_id) ON DELETE CASCADE;


--
-- Name: employee employee_previous_reporting_manager_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_previous_reporting_manager_fkey FOREIGN KEY (previous_reporting_manager) REFERENCES public.employee(employee_id) ON DELETE SET NULL;


--
-- Name: employee employee_reporting_manager_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_reporting_manager_fkey FOREIGN KEY (reporting_manager) REFERENCES public.employee(employee_id) ON DELETE SET NULL;


--
-- Name: lead_assessment_rating lead_assessment_rating_allocation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lead_assessment_rating
    ADD CONSTRAINT lead_assessment_rating_allocation_id_fkey FOREIGN KEY (allocation_id) REFERENCES public.employee_allocation(allocation_id) ON DELETE CASCADE;


--
-- Name: lead_assessment_rating lead_assessment_rating_cycle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lead_assessment_rating
    ADD CONSTRAINT lead_assessment_rating_cycle_id_fkey FOREIGN KEY (cycle_id) REFERENCES public.appraisal_cycle(cycle_id) ON DELETE CASCADE;


--
-- Name: lead_assessment_rating lead_assessment_rating_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lead_assessment_rating
    ADD CONSTRAINT lead_assessment_rating_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employee(employee_id) ON DELETE CASCADE;


--
-- Name: lead_assessment_rating lead_assessment_rating_parameter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lead_assessment_rating
    ADD CONSTRAINT lead_assessment_rating_parameter_id_fkey FOREIGN KEY (parameter_id) REFERENCES public.parameters(parameter_id) ON DELETE CASCADE;


--
-- Name: option option_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.option
    ADD CONSTRAINT option_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.question(question_id) ON DELETE CASCADE;


--
-- Name: parameters parameters_cycle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.parameters
    ADD CONSTRAINT parameters_cycle_id_fkey FOREIGN KEY (cycle_id) REFERENCES public.appraisal_cycle(cycle_id) ON DELETE CASCADE;


--
-- Name: self_assessment_response self_assessment_response_allocation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.self_assessment_response
    ADD CONSTRAINT self_assessment_response_allocation_id_fkey FOREIGN KEY (allocation_id) REFERENCES public.employee_allocation(allocation_id) ON DELETE CASCADE;


--
-- Name: self_assessment_response self_assessment_response_cycle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.self_assessment_response
    ADD CONSTRAINT self_assessment_response_cycle_id_fkey FOREIGN KEY (cycle_id) REFERENCES public.appraisal_cycle(cycle_id) ON DELETE CASCADE;


--
-- Name: self_assessment_response self_assessment_response_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.self_assessment_response
    ADD CONSTRAINT self_assessment_response_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employee(employee_id) ON DELETE CASCADE;


--
-- Name: self_assessment_response self_assessment_response_option_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.self_assessment_response
    ADD CONSTRAINT self_assessment_response_option_id_fkey FOREIGN KEY (option_id) REFERENCES public.option(option_id) ON DELETE CASCADE;


--
-- Name: self_assessment_response self_assessment_response_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.self_assessment_response
    ADD CONSTRAINT self_assessment_response_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.question(question_id) ON DELETE CASCADE;


--
-- Name: stages stages_cycle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stages
    ADD CONSTRAINT stages_cycle_id_fkey FOREIGN KEY (cycle_id) REFERENCES public.appraisal_cycle(cycle_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

