# coding=utf-8
import psycopg2
import bottle 
from bottle import route, run, template, os, static_file, debug, request, redirect

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

@route("/add_customer", method="POST")
def add_customer():
    pno = str(request.forms.get("pno"))
    customer_name = str(request.forms.get("customer_name"))
    email = str(request.forms.get("email"))
    address = str(request.forms.get("address"))
    postno = str(request.forms.get("postno"))
    region = str(request.forms.get("region"))
    total_sales = '0'
    cursor.execute("INSERT INTO customers (pno, customer_name, email, address, postno, region, total_sales) values(%s, %s, %s, %s, %s, %s, %s)", (pno, customer_name, email, address, postno, region, total_sales))
    conn.commit()
    redirect("/customers")

@route("/inventory")
def list_stock():
    sql_get_stock = "SELECT product_name, brand, price, image, supplier, quantity, product_cost, category FROM (products JOIN inventory ON products.product_id=inventory.product_id) WHERE quantity > 0 ORDER BY product_name ASC"
    cursor.execute(sql_get_stock)
    stock = cursor.fetchall()
    return template("inventory", stock=stock)

@route("/out_of_stock")
def list_out_of_stock():
    sql_out_of_stock = "SELECT product_name, brand, price, image, supplier, quantity, product_cost, category FROM (products JOIN inventory ON products.product_id=inventory.product_id) WHERE quantity = 0 ORDER BY product_name ASC"
    cursor.execute(sql_out_of_stock)
    out_of_stock = cursor.fetchall()
    return template("out_of_stock", out_of_stock=out_of_stock)

@route("/sales")
def list_sales():
    sql_products = "SELECT product_id, product_name, brand FROM products"
    cursor.execute(sql_products)
    products = cursor.fetchall()
    return template("sales", products=products)

@route("/suppliers")
def list_supplier():
    sql_supplier = "SELECT * FROM supplier ORDER BY supplier_name ASC"
    cursor.execute(sql_supplier)
    supplier = cursor.fetchall()
    return template("suppliers", supplier=supplier)
    
run(host="127.0.0.1", port=8111)

