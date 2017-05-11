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

    sql_products = "SELECT product_name, description, brand, price, image FROM products"
    cursor.execute(sql_products)
    products = cursor.fetchall()
    
    return template("index.html", products=products)

run(host="127.0.0.1", port=8080)
