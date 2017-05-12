# coding=utf-8
import psycopg2
import bottle 
from bottle import route, run, template, os, static_file

#Konnectar till databsen
conn = psycopg2.connect(dbname="ag8789", user="ag8789", password="cl934pos", host="pgserver.mah.se")

#Pekaren på databasen
cursor = conn.cursor()

#Visar 
@route("/")
def start():
    sql_products = "SELECT product_name, description, brand, price, image FROM products"
    cursor.execute(sql_products)
    products = cursor.fetchall()
    return template("index", products=products)

@route("/sort")
def sort():
    return template("sort")

#Tänker troligtvis fel här. Återkommer
'''
@route("/washer")
def washer():
    sql_washer = "SELECT product_name, description, brand, price, image FROM products WHERE category=tvättmaskin"
    cursor.execute(sql_washer)
    washer = cursor.fetchall()
    return redirect("/sorting", washer=washer)
'''
    
run(host="127.0.0.1", port=8081)
