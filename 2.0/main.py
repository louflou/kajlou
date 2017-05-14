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

#Visar
@route("/")
def start():
    sql_products = "SELECT product_name, description, brand, price, image FROM products"
    cursor.execute(sql_products)
    products = cursor.fetchall()
    return template("index", products=products)


@route("/tvattmaskin")
def sort_category():
    sql_sort_category = "SELECT product_name, description, brand, price, image FROM products WHERE category='tvättmaskin' ORDER BY product_name ASC"
    cursor.execute(sql_sort_category)
    sort_category = cursor.fetchall()
    return template("index", products=sort_category)

@route("/kylskap")
def sort_category():
    sql_sort_category = "SELECT product_name, description, brand, price, image FROM products WHERE category='kylskåp' ORDER BY product_name ASC"
    cursor.execute(sql_sort_category)
    sort_category = cursor.fetchall()
    return template("index", products=sort_category)

@route("/spis")
def sort_category():
    sql_sort_category = "SELECT product_name, description, brand, price, image FROM products WHERE category='spis' ORDER BY product_name ASC"
    cursor.execute(sql_sort_category)
    sort_category = cursor.fetchall()
    return template("index", products=sort_category)

@route("/diskmaskin")
def sort_category():
    sql_sort_category = "SELECT product_name, description, brand, price, image FROM products WHERE category='diskmaskin' ORDER BY product_name ASC"
    cursor.execute(sql_sort_category)
    sort_category = cursor.fetchall()
    return template("index", products=sort_category)

@route("/bosch")
def sort_brand():
    sql_sort_brand = "SELECT product_name, description, brand, price, image FROM products WHERE brand='Bosch' ORDER BY product_name ASC"
    cursor.execute(sql_sort_brand)
    sort_brand = cursor.fetchall()
    return template("index", products=sort_brand)

@route("/electrolux")
def sort_brand():
    sql_sort_brand = "SELECT product_name, description, brand, price, image FROM products WHERE brand='Electrolux' ORDER BY product_name ASC"
    cursor.execute(sql_sort_brand)
    sort_brand = cursor.fetchall()
    return template("index", products=sort_brand)

@route("/sandstrom")
def sort_brand():
    sql_sort_brand = "SELECT product_name, description, brand, price, image FROM products WHERE brand='Sandstrøm' ORDER BY product_name ASC"
    cursor.execute(sql_sort_brand)
    sort_brand = cursor.fetchall()
    return template("index", products=sort_brand)

@route("/candy")
def sort_brand():
    sql_sort_brand = "SELECT product_name, description, brand, price, image FROM products WHERE brand='Candy' ORDER BY product_name ASC"
    cursor.execute(sql_sort_brand)
    sort_brand = cursor.fetchall()
    return template("index", products=sort_brand)

@route("/miele")
def sort_brand():
    sql_sort_brand = "SELECT product_name, description, brand, price, image FROM products WHERE brand='Miele' ORDER BY product_name ASC"
    cursor.execute(sql_sort_brand)
    sort_brand = cursor.fetchall()
    return template("index", products=sort_brand)

@route("/min_pris")
def sort_price():
    sql_sort_price = "SELECT product_name, description, brand, price, image FROM products ORDER BY price asc"
    cursor.execute(sql_sort_price)
    sort_price = cursor.fetchall()
    return template("index", products=sort_price)

@route("/max_pris")
def sort_price():
    sql_sort_price = "SELECT product_name, description, brand, price, image FROM products ORDER BY price desc"
    cursor.execute(sql_sort_price)
    sort_price = cursor.fetchall()
    return template("index", products=sort_price)


#Tänker troligtvis fel här. Återkommer
'''
@route("/washer")
def washer():
    sql_washer = "SELECT product_name, description, brand, price, image FROM products WHERE category=tvättmaskin"
    cursor.execute(sql_washer)
    washer = cursor.fetchall()
    return redirect("/sorting", washer=washer)
'''
    
run(reloader=True, host="127.0.0.1", port=8095)

