# coding=utf-8
import psycopg2
import bottle 
from bottle import route, run, template, os, static_file, debug, request, redirect

#Connectar till databsen
conn = psycopg2.connect(dbname="kajlou", user="ag8789", password="cl934pos", host="pgserver.mah.se")

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

@route("/add_supplier", method="POST")
def add_customer():
    supplier_name = str(request.forms.get("supplier_name"))
    phone = str(request.forms.get("supplier_phone"))
    website = str(request.forms.get("website"))
    cursor.execute("INSERT INTO supplier (supplier_name, phone, website) values(%s, %s, %s)", (supplier_name, phone, website))
    conn.commit()
    redirect("/suppliers")


@route("/add_product", method="POST")
def add_product():
    product_name = str(request.forms.get("product_name"))
    description = str(request.forms.get("description"))
    category = str(request.forms.get("category"))
    image = str(request.forms.get("product_image"))
    brand = str(request.forms.get("brand"))
    price = str(request.forms.get("price"))
    cursor.execute("INSERT INTO products (product_name, description, brand, price, category, image) values(%s, %s, %s, %s, %s, %s)", (product_name, description, brand, price, category, image))
    conn.commit()
    sql_get_product_id = "SELECT last_value FROM products_product_id_seq"
    cursor.execute(sql_get_product_id)
    product_id = cursor.fetchone()
    supplier = str(request.forms.get("supplier"))
    product_cost = str(request.forms.get("cost"))
    quantity = str(request.forms.get("quantity"))
    cursor.execute("INSERT INTO inventory (product_id, supplier, product_cost, quantity) values(%s, %s, %s, %s)", (product_id, supplier, product_cost, quantity))
    conn.commit()
    redirect("/suppliers")


@route("/staff")
def list_staff():
    sql_staff = "SELECT * from staff ORDER BY staff_id ASC"
    cursor.execute(sql_staff)
    staff = cursor.fetchall()
    return template("staff", staff=staff)


@route("/inventory")
def list_stock():
    sql_get_supplier = "SELECT supplier_name FROM supplier"
    cursor.execute(sql_get_supplier)
    suppliers = cursor.fetchall()
    sql_get_stock = "SELECT product_name, brand, price, image, supplier, quantity, product_cost, category, products.product_ID FROM (products JOIN inventory ON products.product_id=inventory.product_id) WHERE quantity > 0 ORDER BY product_name ASC"
    cursor.execute(sql_get_stock)
    stock = cursor.fetchall()
    return template("inventory", stock=stock, suppliers=suppliers)


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
    
run(host="127.0.0.1", port=8112)

