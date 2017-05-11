# coding=utf-8

import psycopg2

# connect
conn = psycopg2.connect(dbname="ag8789", user="ag8789", password="cl934pos", host="pgserver.mah.se")

# create cursor
cursor = conn.cursor()

# execute SQL statement
cursor.execute("select * from staff")

# get the resultset as a tuple
result = cursor.fetchall()

# iterate through resultset
for r in result:
    print(r[1], r[2], r[3], r[4])

