CREATE DATABASE summaries_sk_wikipedia
    WITH 
    OWNER = summaries_sk_wikipedia
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;
    
CREATE TABLE domain
(
    id serial PRIMARY KEY,
    label varchar(20) UNIQUE NOT NULL
)
CREATE TABLE summary
(
    id serial PRIMARY KEY,
    title varchar(50) NOT NULL,
    pageid integer UNIQUE NOT NULL,
    url varchar(100) UNIQUE NOT NULL,
    domain_id integer NOT NULL REFERENCES domain(id) ON DELETE CASCADE ON UPDATE CASCADE
)
CREATE TABLE sentence
(
    id serial PRIMARY KEY,
    rank integer NOT NULL,
    text text NOT NULL,
    summary_id integer NOT NULL  REFERENCES summary(id) ON DELETE CASCADE ON UPDATE CASCADE
)