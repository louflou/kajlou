#coding=utf-8
import psycopg2 #Används för att kopla till databasen
import bottle #Ramverk som används för att underlätta skapandet av en websida
import datetime
from bottle import route, run, template, os, static_file, debug, request, redirect, error,abort

#Konnectar till databsen
conn = psycopg2.connect(dbname="kajlou", user="ag8789", password="cl934pos", host="pgserver.mah.se")

#Pekaren på databasen
cursor = conn.cursor()
    
# Laddar in CSS
@route("/static/<filename:path>")
def send_static(filename):
    return static_file(filename, root="./static/")

#Hanterar 404-fel
@error(404)
def custom404(error):
    error_code = '404'
    return template('error', error_code=error_code)

#Visar startsidan (Tom - endast menyer för val via HTML)
@route("/")
def start():
    return template("index")

#Sorterar kundernas värde utifrån vad de handlat 
@route("/customers")
def list_customers():
    cursor.execute("SELECT pno, customer_name, email, address, postno, region FROM customers ORDER BY customer_name")
    customers = cursor.fetchall()
    return template("customers", customers=customers)

#Funktion som lägger till en kund i databasene med information hätmad från ett formulär i HTML
@route("/customers/value")
def list_customers():
    cursor.execute("SELECT pno, customer_name, email, address, postno, region, SUM(subtotal) FROM customers JOIN sales_details ON pno=customer_id GROUP BY pno ORDER BY SUM(subtotal) DESC")
    customers = cursor.fetchall()
    return template("value", customers=customers)

#Lägger till en kund i databsen
@route("/add_customer", method="POST")
def add_customer():
    pno = str(request.forms.get("pno"))
    customer_name = str(request.forms.get("customer_name"))
    email = str(request.forms.get("email"))
    address = str(request.forms.get("address"))
    postno = str(request.forms.get("postno"))
    region = str(request.forms.get("region"))
    total_sales = "0" #Kunden måste registreras först innan den kan göra ett köp
    cursor.execute("INSERT INTO customers (pno, customer_name, email, address, postno, region, total_sales) VALUES(%s, %s, %s, %s, %s, %s, %s)", (pno, customer_name, email, address, postno, region, total_sales))
    conn.commit()
    redirect("/customers") #Skickas sen till funktionen "customers" som läser in alla kunder på nytt så att användaren kan se att kunden blivit reigstrerad

#Funktion som lägger till en återförsäljare i databsen med infomraiton hämtad från ett formulär i HTML
@route("/add_supplier", method="POST")
def add_customer():
    supplier_name = str(request.forms.get("supplier_name"))
    phone = str(request.forms.get("supplier_phone"))
    website = str(request.forms.get("website"))
    cursor.execute("INSERT INTO supplier (supplier_name, phone, website) VALUES(%s, %s, %s)", (supplier_name, phone, website))
    conn.commit()
    redirect("/suppliers") #Skickar tillbaka användaren till funktionen suppliers så att dem kan se att en återförsäljare blivit adderad i databsaen

#Funktion som registrerar en produkt i datbasen utifrån infomration som hämtas ifrån ett HTML-formulär
@route("/add_product", method="POST")
def add_product():
    try:
        product_name = str(request.forms.get("product_name"))
        description = str(request.forms.get("description"))
        category = str(request.forms.get("category"))
        image = str(request.forms.get("product_image")) 
        brand = str(request.forms.get("brand"))
        price = str(request.forms.get("price"))
        cursor.execute("INSERT INTO products (product_name, description, brand, price, category, image) VALUES(%s, %s, %s, %s, %s, %s)", (product_name, description, brand, price, category, image))
        conn.commit()
        sql_get_product_id = "SELECT last_value FROM products_product_id_seq" #Hämtar senaste använda värdet för att kunna lögga till produkter
        cursor.execute(sql_get_product_id)
        product_id_tup = cursor.fetchone()
        product_id = product_id_tup[0] #Hämtar ut det första värdet i tuplen
        supplier = str(request.forms.get("supplier"))
        product_cost = str(request.forms.get("cost"))
        quantity = str(request.forms.get("quantity"))
        cursor.execute("INSERT INTO inventory (product_id, supplier, product_cost, quantity) VALUES(%s, %s, %s, %s)", (product_id, supplier, product_cost, quantity))
        conn.commit()
        redirect("/inventory") #Skickar tillbaka användaren till funktionen inventory som läser in alla varor på nytt så att användaren kan se att produkten blivit registrerad
    except:
        return template('error')

#Läser in all personal från databsen och ordnar dem efter staff_id
@route("/staff")
def list_staff():
    sql_staff = "SELECT * from staff ORDER BY staff_id ASC"
    cursor.execute(sql_staff)
    staff = cursor.fetchall()
    return template("staff", staff=staff)

#Lägger till en anställd i databsen
@route("/add_staff", method="POST")
def add_staff():
    title = str(request.forms.get("title"))
    staff_name = str(request.forms.get("staff_name"))
    phone = str(request.forms.get("phone"))
    email = str(request.forms.get("email"))
    cursor.execute("INSERT INTO staff (title, staff_name, phone, email) VALUES(%s, %s, %s, %s)", (title, staff_name, phone, email))
    conn.commit()
    redirect("/staff") #Skickas sen till funktionen "staff" som läser in alla anställda på nytt så att admin kan se att den anställde blivit reigstrerad


#Läser in alla varor som finns i lagret
@route("/inventory")
def list_stock():
    sql_get_supplier = "SELECT supplier_name FROM supplier"
    cursor.execute(sql_get_supplier)
    suppliers = cursor.fetchall()
    sql_get_stock = "SELECT product_name, brand, price, image, supplier, quantity, product_cost, category, products.product_ID FROM (products JOIN inventory ON products.product_id=inventory.product_id) WHERE quantity > 0 ORDER BY product_ID ASC"
    cursor.execute(sql_get_stock)
    stock = cursor.fetchall()
    return template("inventory", stock=stock, suppliers=suppliers)

#Funktion som används om man köper in fler av en produkt och uppdaterar quantity för dem i databasen
@route("/update_product", method="POST")
def update_existing():
    product_id = str(request.forms.get("x_product_id"))
    supplier = str(request.forms.get("x_supplier"))
    quantity = int(request.forms.get("x_quantity"))
    cursor.execute("SELECT quantity FROM inventory WHERE product_id = %s AND supplier = %s", (product_id, supplier))
    current_quantity_tup = cursor.fetchone()
    current_quantity = int(current_quantity_tup[0])
    cursor.execute("UPDATE inventory SET quantity = %s WHERE product_id = %s AND supplier = %s", (quantity+current_quantity, product_id, supplier))
    conn.commit()
    redirect("/inventory")
    
#Läser in alla varor i lagret där quantity är mindre än 0 för att se vilka registrerade varor som inte finns på lager
@route("/out_of_stock")
def list_out_of_stock():
    sql_out_of_stock = "SELECT product_name, brand, price, image, supplier, quantity, product_cost, category, products.product_id FROM (products JOIN inventory ON products.product_id=inventory.product_id) WHERE quantity = 0 ORDER BY product_name ASC"
    cursor.execute(sql_out_of_stock)
    out_of_stock = cursor.fetchall()
    return template("out_of_stock", out_of_stock=out_of_stock)


#Läser in alla kvitton med försäljningar som gjorts
@route("/sales")    
def list_sales():
    cursor.execute("SELECT sales_id, customer_id, staff_id, subtotal, sales_date FROM sales_details ORDER BY sales_id DESC")
    start = cursor.fetchall()
    products = {} #Skapar ett lexikon för alla köp
    for row in start:
        receipt = str(row[0]) 
        cursor.execute("SELECT products.product_id, category, brand, price, quantity FROM sales JOIN products ON sales.product_id=products.product_id WHERE sales_id = {}".format(receipt))
        plist = cursor.fetchall()
        products[receipt] = plist #Använder sales_id som nyckel i lexikonet för alla produkter
    return template("sales", start=start, products=products)

#Påbörjar en försäljning genom att registrerar en säljare och kund i tabellen sales_details
@route("/begin_sales", method="POST")
def reg_sales():
    customer = str(request.forms.get("customer_id"))
    vendor = str(request.forms.get("staff_id"))
    cursor.execute("INSERT INTO sales_details(customer_id, staff_id) VALUES(%s, %s)", (customer, vendor))
    conn.commit()
    redirect("/sales")

#Lägger till varor för kvittot kopplat till sales_details
@route("/add_product_to_sales", method="POST")
def add_to_sales():
    sql_get_sales_id = "SELECT last_value FROM sales_details_sales_id_seq"
    cursor.execute(sql_get_sales_id)
    sales_id_tup = cursor.fetchone()
    sales_id = int(sales_id_tup[0])
    product_id = str(request.forms.get("product_id"))
    quantity = str(request.forms.get("quantity"))
    
    if int(current_quantity) >= int(quantity): #Om antalet produkter är fler eller lika många som de som vill köpas
        new_quantity = int(current_quantity) - int(quantity)
        cursor.execute("INSERT INTO sales(sales_id, product_id, quantity) VALUES(%s, %s, %s)", (sales_id, product_id, quantity))
        cursor.execute("UPDATE inventory SET quantity = {} WHERE product_id = {} AND quantity >= {}".format(new_quantity, product_id, new_quantity))
        conn.commit()
        redirect("/sales")
    else:
        redirect("/error_quantity")

#Visas om användaren försöker köpa fler produkter av en vara än vad som är registrerat i databasen
@route("/error_quantity")
def error():
    return template('error_quantity')

#Avslutar köpet
@route("/finish_sales", method="POST")
def finish_sales():
    cursor.execute("SELECT last_value FROM sales_details_sales_id_seq")
    sales_id_tup = cursor.fetchone()
    sales_id = sales_id_tup[0]
    cursor.execute("SELECT SUM(quantity * price) FROM sales JOIN products ON sales.product_id=products.product_id WHERE sales_id={}".format(sales_id))
    total_tup = cursor.fetchone()
    subtotal = total_tup[0]

    now = datetime.datetime.now() #Hämtar dagens datum och tid 
    get_date = now.strftime("%Y-%m-%d")
    date = str(get_date)
    
    cursor.execute("UPDATE sales_details SET subtotal = {0}, sales_date = '{1}' WHERE sales_id = {2}".format(subtotal, date, sales_id))
    conn.commit()
    redirect("/sales")
    
#Läser in alla återfärsäljare som är registrerade i databasen
@route("/suppliers")
def list_supplier():
    sql_supplier = "SELECT * FROM supplier ORDER BY supplier_name ASC"
    cursor.execute(sql_supplier)
    supplier = cursor.fetchall()
    return template("suppliers", supplier=supplier)

#Kör systemet på följande address
run(host="127.0.0.1", port=8112)
