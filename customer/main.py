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

def get_cat():
    ''' Hämtar värden för kategori till menylänkarna för sök-filter'''
    sql_category = "SELECT DISTINCT category FROM (products JOIN inventory ON products.product_id=inventory.product_id) WHERE quantity > 0 ORDER BY category"
    cursor.execute(sql_category)
    category = cursor.fetchall()
    return category

def get_brand():
    ''' Hämtar värden för märken till menylänkarna för sök-filter'''
    sql_brand = "SELECT DISTINCT brand FROM (products JOIN inventory ON products.product_id=inventory.product_id) WHERE quantity > 0 ORDER BY brand"
    cursor.execute(sql_brand)
    brand = cursor.fetchall()
    return brand

#Startsidan som läser in alla produkter som finns till salu i lagret
@route("/")
def start():
    sql_products = "SELECT DISTINCT product_name, description, brand, price, image, category FROM (products JOIN inventory ON products.product_id=inventory.product_id) WHERE quantity > 0 ORDER BY product_name"
    cursor.execute(sql_products)
    products = cursor.fetchall()
    category = get_cat()
    brand = get_brand()
    return template("index", products=products, category=category, brand=brand)

#Sorterar varorna i lagret efter kategorin som användaren väljer
@route("/category/<category>")
def sort_category(category):
    sql_sort_category = "SELECT product_name, description, brand, price, image, category FROM (products JOIN inventory ON products.product_id=inventory.product_id) WHERE quantity > 0 AND category= %s ORDER BY product_name ASC"
    cursor.execute(sql_sort_category, [category])
    products = cursor.fetchall()
    category = get_cat()
    brand = get_brand()
    return template("category", products=products, category=category, brand=brand)

#Sorterar varorna efter märket som användaren väljer
@route("/brand/<brand>")
def sort_brand(brand):
    sql_sort_brand = "SELECT product_name, description, brand, price, image FROM (products JOIN inventory ON products.product_id=inventory.product_id) WHERE quantity > 0 AND brand = %s ORDER BY product_name ASC"
    cursor.execute(sql_sort_brand, [brand])
    products = cursor.fetchall()
    category = get_cat()
    brand = get_brand()
    return template("brand", products=products, category=category, brand=brand)

#Sorterar varorna efter pris - minst till störst
@route("/min_pris")
def sort_price():
    sql_sort_price = "SELECT product_name, description, brand, price, image FROM (products JOIN inventory ON products.product_id=inventory.product_id) WHERE quantity > 0 ORDER BY price ASC"
    cursor.execute(sql_sort_price)
    products = cursor.fetchall()
    category = get_cat()
    brand = get_brand()
    return template("price", products=products, category=category, brand=brand)

#Soreterar varorna efter pris - störst till minst
@route("/max_pris")
def sort_price():
    sql_sort_price = "SELECT product_name, description, brand, price, image FROM (products JOIN inventory ON products.product_id=inventory.product_id) WHERE quantity > 0 ORDER BY price DESC"
    cursor.execute(sql_sort_price)
    products = cursor.fetchall()
    category = get_cat()
    brand = get_brand()
    return template("price", products=products, category=category, brand=brand)

#Hittar produkten efter produktnamnet som användaren sökte på
@route("/search", method="POST")
def list_search():
    category = get_cat()
    brand = get_brand()
    user_input = str(request.forms.get("search"))
    sql_search = "SELECT product_name, description, brand, price, image FROM products WHERE product_name LIKE '%{}%'".format(user_input)
    cursor.execute(sql_search)
    search = cursor.fetchall()
    return template("search", search=search, category=category, brand=brand)

#Kör systemet på följande address 
run(host="127.0.0.1", port=8107)

