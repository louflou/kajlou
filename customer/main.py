# coding=utf-8
import psycopg2 #Används för att skapa en koppling till databasen
import bottle #Ramverk för att underlätta skapandet av en hemsida
from bottle import route, run, template, os, static_file, debug, request

#Konnectar till databsen
conn = psycopg2.connect(dbname="kajlou", user="ag8789", password="cl934pos", host="pgserver.mah.se")

#Pekaren på databasen
cursor = conn.cursor()

# Laddar in CSS
@route("/static/<filename:path>")
def send_static(filename):
    return static_file(filename, root="./static/")

#Startsidan som läser in alla produkter som finns till salu i lagret
@route("/")
def start():
    sql_products = "SELECT product_name, description, brand, price, image, category FROM products"
    cursor.execute(sql_products)
    products = cursor.fetchall()
    
    sql_category = "SELECT DISTINCT category FROM products ORDER BY category"
    cursor.execute(sql_category)
    category = cursor.fetchall()

    sql_brand = "SELECT DISTINCT brand FROM products ORDER BY brand"
    cursor.execute(sql_brand)
    brand = cursor.fetchall()
    
    return template("index", products=products, category=category, brand=brand)

#Sorterar varorna i lagret efter kategorin som användaren väljer
@route("/category/<category>")
def sort_category(category):
    sql_sort_category = "SELECT product_name, description, brand, price, image, category FROM products WHERE category= %s ORDER BY product_name ASC"
    cursor.execute(sql_sort_category, [category])
    products = cursor.fetchall()

    sql_category = "SELECT DISTINCT category FROM products ORDER BY category"
    cursor.execute(sql_category)
    category = cursor.fetchall()

    sql_brand = "SELECT DISTINCT brand FROM products ORDER BY brand"
    cursor.execute(sql_brand)
    brand = cursor.fetchall()

    return template("category", products=products, category=category, brand=brand)

#Sorterar varorna efter märket som användaren väljer
@route("/brand/<brand>")
def sort_brand(brand):
    sql_sort_brand = "SELECT product_name, description, brand, price, image FROM products WHERE brand = %s ORDER BY product_name ASC"
    cursor.execute(sql_sort_brand, [brand])
    products = cursor.fetchall()

    sql_category = "SELECT DISTINCT category FROM products ORDER BY category"
    cursor.execute(sql_category)
    category = cursor.fetchall()

    sql_brand = "SELECT DISTINCT brand FROM products ORDER BY brand"
    cursor.execute(sql_brand)
    brand = cursor.fetchall()

    return template("brand", products=products, category=category, brand=brand)

#Sorterar varorna efter pris - minst till störst
@route("/min_pris")
def sort_price():
    sql_sort_price = "SELECT product_name, description, brand, price, image FROM products ORDER BY price ASC"
    cursor.execute(sql_sort_price)
    products = cursor.fetchall()

    sql_category = "SELECT DISTINCT category FROM products ORDER BY category"
    cursor.execute(sql_category)
    category = cursor.fetchall()

    sql_brand = "SELECT DISTINCT brand FROM products ORDER BY brand"
    cursor.execute(sql_brand)
    brand = cursor.fetchall()
    return template("price", products=products, category=category, brand=brand)

#Soreterar varorna efter pris - störst till minst
@route("/max_pris")
def sort_price():
    sql_sort_price = "SELECT product_name, description, brand, price, image FROM products ORDER BY price DESC"
    cursor.execute(sql_sort_price)
    products = cursor.fetchall()

    sql_category = "SELECT DISTINCT category FROM products ORDER BY category"
    cursor.execute(sql_category)
    category = cursor.fetchall()

    sql_brand = "SELECT DISTINCT brand FROM products ORDER BY brand"
    cursor.execute(sql_brand)
    brand = cursor.fetchall()
    return template("price", products=products, category=category, brand=brand)

#Hittar märken och/eller kategorier som användaren sökte på
@route("/search", method="POST")
def list_search():
    sql_category = "SELECT DISTINCT category FROM products ORDER BY vategory"
    cursor.execute(sql_category)
    category = cursor.fetchall()

    sql_brand = "SELECT DISTINCT brand FROM products ORDER BY brand"
    cursor.execute(sql_brand)
    brand = cursor.fetchall()
   
    user_input = str(request.forms.get("search"))
    sql_search = "SELECT product_name, description, brand, price, image FROM products WHERE product_name LIKE '%{}%'".format(user_input)
    cursor.execute(sql_search)
    search = cursor.fetchall()
    print(search)
    return template("search", search=search, category=category, brand=brand)

#Kör systemet på följande address 
run(host="127.0.0.1", port=8100)

