# coding=utf-8
import psycopg2
import bottle 
from bottle import route, run, template, os, static_file, debug

#Konnectar till databsen
conn = psycopg2.connect(dbname="ag8789", user="ag8789", password="cl934pos", host="pgserver.mah.se")

#Pekaren på databasen
cursor = conn.cursor()

# Laddar in CSS
@route("/static/<filename:path>")
def send_static(filename):
    return static_file(filename, root="./static/")


@route("/")
def start():
    return template("index")

@route("/customers")
def list_customers():
    sql_customers = "SELECT * FROM customers"
    cursor.execute(sql_customers)
    customers = cursor.fetchall()
    return template("customers", customers=customers)

@route("/inventory")
def list_products():
    return template("inventory")

@route("/sales")
def list_sales():
    return template("sales")

@route("/suppliers")
def list_suppliers():
    return template("suppliers")
    
run(host="127.0.0.1", port=8106)

