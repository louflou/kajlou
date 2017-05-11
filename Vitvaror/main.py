# coding=utf-8
import psycopg2
import bottle
from bottle import route, run, template, os

# connect
conn = psycopg2.connect(dbname="ag8789", user="ag8789", password="cl934pos", host="pgserver.mah.se")

# create cursor
cursor = conn.cursor()

@route("/")
def start():
    return template("index.html")

run(host="127.0.0.1", port=8080)
