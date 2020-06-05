--
-- PostgreSQL database dump
--

-- Dumped from database version 12.1
-- Dumped by pg_dump version 12.1

-- Started on 2020-05-03 16:11:20

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

SET default_table_access_method = heap;

--
-- TOC entry 202 (class 1259 OID 16407)
-- Name: last_run; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.last_run (
    lock character(1) NOT NULL,
    date date NOT NULL,
    CONSTRAINT ck_t1_locked CHECK ((lock = 'X'::bpchar))
);


ALTER TABLE public.last_run OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 16441)
-- Name: times; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.times (
    id integer NOT NULL,
    date date NOT NULL,
    minutes integer
);


ALTER TABLE public.times OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 16439)
-- Name: times_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.times_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.times_id_seq OWNER TO postgres;

--
-- TOC entry 2833 (class 0 OID 0)
-- Dependencies: 203
-- Name: times_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.times_id_seq OWNED BY public.times.id;


--
-- TOC entry 2692 (class 2604 OID 16444)
-- Name: times id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.times ALTER COLUMN id SET DEFAULT nextval('public.times_id_seq'::regclass);


--
-- TOC entry 2825 (class 0 OID 16407)
-- Dependencies: 202
-- Data for Name: last_run; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.last_run (lock, date) FROM stdin;
X	2020-05-03
\.

--
-- TOC entry 2834 (class 0 OID 0)
-- Dependencies: 203
-- Name: times_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.times_id_seq', 90, true);


--
-- TOC entry 2694 (class 2606 OID 16412)
-- Name: last_run pk_t1; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.last_run
    ADD CONSTRAINT pk_t1 PRIMARY KEY (lock);


--
-- TOC entry 2696 (class 2606 OID 16448)
-- Name: times times_date_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.times
    ADD CONSTRAINT times_date_key UNIQUE (date);


--
-- TOC entry 2698 (class 2606 OID 16446)
-- Name: times times_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.times
    ADD CONSTRAINT times_pkey PRIMARY KEY (id);



