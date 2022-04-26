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
-- Name: altphrases id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.altphrases ALTER COLUMN id SET DEFAULT nextval('public.altphrases_id_seq'::regclass);


--
-- Name: keyphrases id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.keyphrases ALTER COLUMN id SET DEFAULT nextval('public.keyphrases_id_seq'::regclass);


--
-- Data for Name: altphrases; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.altphrases (id, phrase, fid) FROM stdin;
10	 was hab ich zu erledigen 	5
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
26	 oeffne auf youtube 	8
27	 mach nicht 	2
6	 suche nach 	3
31	 suche bitte nach 	3
32	 google nach 	3
34	 google bitte nach 	3
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
\.


--
-- Name: altphrases_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.altphrases_id_seq', 34, true);


--
-- Name: keyphrases_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.keyphrases_id_seq', 8, true);


--
-- Name: altphrases altphrases_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.altphrases
    ADD CONSTRAINT altphrases_pk PRIMARY KEY (id);


--
-- Name: keyphrases keyphrases_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.keyphrases
    ADD CONSTRAINT keyphrases_pk PRIMARY KEY (id);


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
-- PostgreSQL database dump complete
--

