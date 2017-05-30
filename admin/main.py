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
    product_id_tup = cursor.fetchone()
    product_id = product_id_tup[0]
    supplier = str(request.forms.get("supplier"))
    product_cost = str(request.forms.get("cost"))
    quantity = str(request.forms.get("quantity"))
    cursor.execute("INSERT INTO inventory (product_id, supplier, product_cost, quantity) values(%s, %s, %s, %s)", (product_id, supplier, product_cost, quantity))
    conn.commit()
    redirect("/inventory")

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
    

@route("/out_of_stock")
def list_out_of_stock():
    sql_out_of_stock = "SELECT product_name, brand, price, image, supplier, quantity, product_cost, category FROM (products JOIN inventory ON products.product_id=inventory.product_id) WHERE quantity = 0 ORDER BY product_name ASC"
    cursor.execute(sql_out_of_stock)
    out_of_stock = cursor.fetchall()
    return template("out_of_stock", out_of_stock=out_of_stock)

@route("/sales")    
def list_sales():
    sql_get_sales = "SELECT sales_details.sales_id, product_id, quantity, customer_id, staff_id, date FROM (sales JOIN sales_details ON sales.sales_id=sales_details.sales_id)"
    cursor.execute(sql_get_sales)
    get_sales = cursor.fetchall()
    return template("sales", get_sales=get_sales)

@route("/begin_sales", method="POST")
def reg_sales():
    customer = str(request.forms.get("customer_id"))
    vendor = str(request.forms.get("staff_id"))
    cursor.execute("INSERT INTO sales_details(customer_id, staff_id) values(%s, %s)", (customer, vendor))
    conn.commit()
    redirect("/sales")


@route("/add_product_to_sales", method="POST")
def add_to_sales():
    sql_get_sales_id = "SELECT last_value FROM sales_details_sales_id_seq"
    cursor.execute(sql_get_sales_id)
    sales_id_tup = cursor.fetchone()
    sales_id = int(sales_id_tup[0])
    product_id = str(request.forms.get("product_id"))
    quantity = str(request.forms.get("quantity"))
    cursor.execute("INSERT INTO sales (sales_id, product_id, quantity) values(‰s, ‰s, ‰s)", (sales_id, product_id, quantity))
    conn.commit()
    redirect("/sales")
    

@route("/suppliers")
def list_supplier():
    sql_supplier = "SELECT * FROM supplier ORDER BY supplier_name ASC"
    cursor.execute(sql_supplier)
    supplier = cursor.fetchall()
    return template("suppliers", supplier=supplier)
    
run(host="127.0.0.1", port=8112)

