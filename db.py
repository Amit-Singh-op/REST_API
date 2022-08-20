import sqlite3

conn = sqlite3.connect("user_details.sqlite")

cursor = conn.cursor()
sql_query = """ CREATE TABLE user (
    id integer PRIMARY KEY,
    first_name text NOT NULL,
    last_name text NOT NULL,
    company_name text NOT NULL,
    age integer NOT NULL,
    city text NOT NULL,
    state text NOT NULL,
    zip integer NOT NULL,
    email text NOT NULL,
    web text NOT NULL
)"""
cursor.execute(sql_query)