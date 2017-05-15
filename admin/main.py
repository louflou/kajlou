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
    sql_customers = "SELECT * FROM customers ORDER BY total_sales DESC"
    cursor.execute(sql_customers)
    customers = cursor.fetchall()
    return template("customers", customers=customers)

@route("/customers/name")
def list_customers():
    sql_customers = "SELECT * FROM customers ORDER BY customer_name ASC"
    cursor.execute(sql_customers)
    customers = cursor.fetchall()
    return template("customers", customers=customers)

@route("/customers/region")
def list_customers():
    sql_customers = "SELECT * FROM customers ORDER BY region ASC"
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
def list_supplier():
    sql_supplier = "SELECT * FROM supplier ORDER BY supplier_name ASC"
    cursor.execute(sql_supplier)
    supplier = cursor.fetchall()
    return template("suppliers", supplier=supplier)
    
run(host="127.0.0.1", port=8108)

