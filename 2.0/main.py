# coding=utf-8
import psycopg2
import bottle
from bottle import route, run, template, os, static_file

# connect
conn = psycopg2.connect(dbname="ag8789", user="ag8789", password="cl934pos", host="pgserver.mah.se")

# create cursor
cursor = conn.cursor()

@route("/")
def start():
    print('test')
    sql_products = "SELECT product_name, description, brand, price, image FROM products"
    cursor.execute(sql_products)
    products = cursor.fetchall()
    print('test1')
    return template("bajs", products=products)

run(host="127.0.0.1", port=8081)
