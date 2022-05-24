--
-- PostgreSQL database dump
--

-- Dumped from database version 13.4
-- Dumped by pg_dump version 13.4

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

--
-- Name: add_altphrase(character varying, character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.add_altphrase(altphrase character varying, tokeyphrase character varying) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
begin
    insert into altphrases (fid, phrase)
    values ((select id from keyphrases where phrase = toKeyphrase), ' ' || altphrase || ' ');
    return 'Erfolgreich erstellt';

exception
    when NOT_NULL_VIOLATION THEN
        return 'Diese Keyphrase gibt es nicht!';

end;
$$;


ALTER FUNCTION public.add_altphrase(altphrase character varying, tokeyphrase character varying) OWNER TO postgres;

--
-- Name: createnewplan(character varying, integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.createnewplan(notiz character varying, userid integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
BEGIN
    insert into Trainingsplan (Notiz, ID)
    VALUES (notiz, userID);

    return 'Trainingsplan erfolgreich erstellt!';

exception
    when FOREIGN_KEY_VIOLATION THEN
        return 'Dieser Nutzer existiert nicht!';

    when string_data_right_truncation then
        return 'Notiz ist zu lang!';

END;
$$;


ALTER FUNCTION public.createnewplan(notiz character varying, userid integer) OWNER TO postgres;

--
-- Name: get_keyphrase(character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_keyphrase(altphrase character varying) RETURNS TABLE(phrase character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
    return query (
        select k.phrase from keyphrases k join altphrases a on k.id = a.fid
            where a.phrase = altphrase);

End;
$$;


ALTER FUNCTION public.get_keyphrase(altphrase character varying) OWNER TO postgres;

--
-- Name: getkeyphrase(character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.getkeyphrase(altphrase character varying) RETURNS text
    LANGUAGE plpgsql
    AS $$
BEGIN
    return (select phrase from keyphrases
where id = (select fid from altphrases where altphrases.phrase like altPhrase));

end;
$$;


ALTER FUNCTION public.getkeyphrase(altphrase character varying) OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: nutzer_in; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.nutzer_in (
    id integer NOT NULL,
    nutzername character varying(25) NOT NULL,
    vorname character varying(20),
    nachname character varying(20)
);


ALTER TABLE public.nutzer_in OWNER TO postgres;

--
-- Name: trainingsplan; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.trainingsplan (
    plan_id integer NOT NULL,
    titel character varying(50) NOT NULL,
    notiz character varying(150) NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.trainingsplan OWNER TO postgres;

--
-- Name: allplans; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.allplans AS
 SELECT trainingsplan.titel AS plan,
    ni.nutzername AS account
   FROM (public.trainingsplan
     JOIN public.nutzer_in ni ON ((trainingsplan.id = ni.id)));


ALTER TABLE public.allplans OWNER TO postgres;

--
-- Name: altphrases; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.altphrases (
    id integer NOT NULL,
    phrase character varying NOT NULL,
    fid integer NOT NULL
);


ALTER TABLE public.altphrases OWNER TO postgres;

--
-- Name: altphrases_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.altphrases_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.altphrases_id_seq OWNER TO postgres;

--
-- Name: altphrases_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.altphrases_id_seq OWNED BY public.altphrases.id;


--
-- Name: beinhaltet; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.beinhaltet (
    plan_id integer NOT NULL,
    uebungs_id integer NOT NULL
);


ALTER TABLE public.beinhaltet OWNER TO postgres;

--
-- Name: fuehrt_durch; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fuehrt_durch (
    saetze integer NOT NULL,
    wiederholunge integer NOT NULL,
    gewichtkg numeric NOT NULL,
    id integer NOT NULL,
    uebungs_id integer NOT NULL
);


ALTER TABLE public.fuehrt_durch OWNER TO postgres;

--
-- Name: keyphrases; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.keyphrases (
    id integer NOT NULL,
    phrase character varying NOT NULL
);


ALTER TABLE public.keyphrases OWNER TO postgres;

--
-- Name: keyphrases_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.keyphrases_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.keyphrases_id_seq OWNER TO postgres;

--
-- Name: keyphrases_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.keyphrases_id_seq OWNED BY public.keyphrases.id;


--
-- Name: nutzer_in_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.nutzer_in_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.nutzer_in_id_seq OWNER TO postgres;

--
-- Name: nutzer_in_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.nutzer_in_id_seq OWNED BY public.nutzer_in.id;


--
-- Name: trainingsplan_plan_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.trainingsplan_plan_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trainingsplan_plan_id_seq OWNER TO postgres;

--
-- Name: trainingsplan_plan_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.trainingsplan_plan_id_seq OWNED BY public.trainingsplan.plan_id;


--
-- Name: uebung; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.uebung (
    uebungs_id integer NOT NULL,
    bezeichnung character varying(30) NOT NULL,
    durchfuehrungsbeschreibung character varying(350) NOT NULL
);


ALTER TABLE public.uebung OWNER TO postgres;

--
-- Name: uebung_uebungs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.uebung_uebungs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.uebung_uebungs_id_seq OWNER TO postgres;

--
-- Name: uebung_uebungs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.uebung_uebungs_id_seq OWNED BY public.uebung.uebungs_id;


--
-- Name: altphrases id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.altphrases ALTER COLUMN id SET DEFAULT nextval('public.altphrases_id_seq'::regclass);


--
-- Name: keyphrases id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.keyphrases ALTER COLUMN id SET DEFAULT nextval('public.keyphrases_id_seq'::regclass);


--
-- Name: nutzer_in id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.nutzer_in ALTER COLUMN id SET DEFAULT nextval('public.nutzer_in_id_seq'::regclass);


--
-- Name: trainingsplan plan_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.trainingsplan ALTER COLUMN plan_id SET DEFAULT nextval('public.trainingsplan_plan_id_seq'::regclass);


--
-- Name: uebung uebungs_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.uebung ALTER COLUMN uebungs_id SET DEFAULT nextval('public.uebung_uebungs_id_seq'::regclass);


--
-- Data for Name: altphrases; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.altphrases (id, phrase, fid) FROM stdin;
11	 was ist noch zu tuen 	5
3	 google 	3
2	 nein 	2
4	 na klar 	1
5	 auf keinen fall 	2
1	 ja 	1
9	 classroom 	4
7	 niemals 	2
12	 wikipedia 	6
13	 wer ist 	6
14	 was ist 	6
15	 suche auf wikipedia 	6
18	 suche auf google 	3
19	 sicher nicht 	2
20	 bitte 	1
21	 mach 	1
22	 youtube 	7
23	 suche auf youtube 	7
24	 zeig mir 	8
25	 spiel ab 	8
27	 mach nicht 	2
6	 suche nach 	3
31	 suche bitte nach 	3
32	 google nach 	3
34	 google bitte nach 	3
26	 öffne auf youtube 	8
10	 was habe ich zu erledigen 	5
36	 wetter 	10
35	 rechner 	9
39	 wieviel ist 	9
40	 zeige mir 	8
41	 spiel 	8
42	 spiele 	8
43	 zeige mir das erste video zu 	8
44	 zeig mir das erste video zu 	8
45	 zeig mir etwas zu 	8
46	 zeige mir etwas zu 	8
47	 suche auf youtube nach 	7
48	 such auf youtube nach 	7
49	 finde auf youtube 	7
50	 find auf youtube 	7
51	 find 	7
52	 finde 	7
53	 suche bitte auf youtube nach 	7
54	 such bitte auf youtube nach 	7
55	 ja bitte 	1
57	 was ergibt 	9
56	 wie viel ist 	9
58	 errate 	13
\.


--
-- Data for Name: beinhaltet; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.beinhaltet (plan_id, uebungs_id) FROM stdin;
\.


--
-- Data for Name: fuehrt_durch; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fuehrt_durch (saetze, wiederholunge, gewichtkg, id, uebungs_id) FROM stdin;
\.


--
-- Data for Name: keyphrases; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.keyphrases (id, phrase) FROM stdin;
4	classroom
3	google
5	erledigen
2	nein
1	ja
6	wikipedia
7	youtube
8	youtube abspielen
9	rechner
10	wetter
13	prediction
\.


--
-- Data for Name: nutzer_in; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.nutzer_in (id, nutzername, vorname, nachname) FROM stdin;
\.


--
-- Data for Name: trainingsplan; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.trainingsplan (plan_id, titel, notiz, id) FROM stdin;
\.


--
-- Data for Name: uebung; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.uebung (uebungs_id, bezeichnung, durchfuehrungsbeschreibung) FROM stdin;
\.


--
-- Name: altphrases_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.altphrases_id_seq', 58, true);


--
-- Name: keyphrases_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.keyphrases_id_seq', 13, true);


--
-- Name: nutzer_in_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.nutzer_in_id_seq', 1, false);


--
-- Name: trainingsplan_plan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.trainingsplan_plan_id_seq', 1, false);


--
-- Name: uebung_uebungs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.uebung_uebungs_id_seq', 1, false);


--
-- Name: altphrases altphrases_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.altphrases
    ADD CONSTRAINT altphrases_pk PRIMARY KEY (id);


--
-- Name: beinhaltet beinhaltet_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.beinhaltet
    ADD CONSTRAINT beinhaltet_pkey PRIMARY KEY (plan_id, uebungs_id);


--
-- Name: fuehrt_durch fuehrt_durch_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fuehrt_durch
    ADD CONSTRAINT fuehrt_durch_pkey PRIMARY KEY (id, uebungs_id);


--
-- Name: keyphrases keyphrases_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.keyphrases
    ADD CONSTRAINT keyphrases_pk PRIMARY KEY (id);


--
-- Name: nutzer_in nutzer_in_nutzername_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.nutzer_in
    ADD CONSTRAINT nutzer_in_nutzername_key UNIQUE (nutzername);


--
-- Name: nutzer_in nutzer_in_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.nutzer_in
    ADD CONSTRAINT nutzer_in_pkey PRIMARY KEY (id);


--
-- Name: trainingsplan trainingsplan_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.trainingsplan
    ADD CONSTRAINT trainingsplan_pkey PRIMARY KEY (plan_id);


--
-- Name: uebung uebung_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.uebung
    ADD CONSTRAINT uebung_pkey PRIMARY KEY (uebungs_id);


--
-- Name: altphrases_id_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX altphrases_id_uindex ON public.altphrases USING btree (id);


--
-- Name: altphrases altphrases_keyphrases_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.altphrases
    ADD CONSTRAINT altphrases_keyphrases_id_fk FOREIGN KEY (fid) REFERENCES public.keyphrases(id);


--
-- Name: beinhaltet beinhaltet_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.beinhaltet
    ADD CONSTRAINT beinhaltet_plan_id_fkey FOREIGN KEY (plan_id) REFERENCES public.trainingsplan(plan_id);


--
-- Name: beinhaltet beinhaltet_uebungs_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.beinhaltet
    ADD CONSTRAINT beinhaltet_uebungs_id_fkey FOREIGN KEY (uebungs_id) REFERENCES public.uebung(uebungs_id);


--
-- Name: fuehrt_durch fuehrt_durch_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fuehrt_durch
    ADD CONSTRAINT fuehrt_durch_id_fkey FOREIGN KEY (id) REFERENCES public.nutzer_in(id);


--
-- Name: fuehrt_durch fuehrt_durch_uebungs_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fuehrt_durch
    ADD CONSTRAINT fuehrt_durch_uebungs_id_fkey FOREIGN KEY (uebungs_id) REFERENCES public.uebung(uebungs_id);


--
-- Name: trainingsplan trainingsplan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.trainingsplan
    ADD CONSTRAINT trainingsplan_id_fkey FOREIGN KEY (id) REFERENCES public.nutzer_in(id);


--
-- PostgreSQL database dump complete
--

