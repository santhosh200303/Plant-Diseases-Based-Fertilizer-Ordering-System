from flask import Flask, render_template, request, redirect, flash, session
from flask import Flask, render_template, request, redirect, url_for, flash,session,jsonify
from datetime import datetime
from PIL import Image
import mysql.connector
import CNN
import os
import numpy as np
import torch
import pandas as pd
import torchvision.transforms.functional as TF
import random
import string

def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

disease_info = pd.read_csv('disease_info.csv' , encoding='cp1252')
supplement_info = pd.read_csv('supplement_info.csv',encoding='cp1252')

model = CNN.CNN(39)    
model.load_state_dict(torch.load("plant_disease_model_1_latest.pt"))
model.eval()

def prediction(image_path):
    image = Image.open(image_path)
    image = image.resize((224, 224))
    input_data = TF.to_tensor(image)
    input_data = input_data.view((-1, 3, 224, 224))
    output = model(input_data)
    output = output.detach().numpy()
    index = np.argmax(output)
    return index


app = Flask(__name__,)
app.secret_key = 'Santhosh032003@'

# MySQL Database Connection
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',        # Default MySQL username (root)
        password='',        # Default MySQL password (empty)
        database='fs'  # Name of your database
    )
    return conn
print("database connected successfully")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        image = request.files['image']
        filename = image.filename
        file_path = os.path.join('static/uploads', filename)
        image.save(file_path)
        print(file_path)
        pred = prediction(file_path)
        title = disease_info['disease_name'][pred]
        description =disease_info['description'][pred]
        prevent = disease_info['Possible Steps'][pred]
        image_url = disease_info['image_url'][pred]
        supplement_name = supplement_info['supplement name'][pred]
       
        return render_template('submit.html' , title = title , desc = description , prevent = prevent , 
                               image_url = image_url , pred = pred ,sname = supplement_name )

@app.route('/upload')
def ai_engine_page():
    return render_template('upload.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connect to MySQL and check admin credentials
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password))
        admin = cursor.fetchone()
        conn.close()

        if admin:
            session['admin'] = admin[0]  # Store admin ID or other data in session
            flash('Login successful!', 'success')
            return redirect('/ad_dashboard')  # Redirect to admin dashboard
        else:
            flash('Invalid username or password', 'danger')

    return render_template('index.html')



@app.route('/ad_dashboard')
def ad_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch totals for different entities
    cursor.execute('SELECT COUNT(*) FROM products')
    product_total = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM feedback')
    feedback_total = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM sale_order')
    purchase_total = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM sale_transaction')
    sale_total = cursor.fetchone()[0]

    conn.close()

    # Render the dashboard with totals
    return render_template(
        'ad_dashboard.html', 
        product_total=product_total, 
        feedback_total=feedback_total, 
        purchase_total=purchase_total, 
        sale_total=sale_total
    )

@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch totals for different entities
    cursor.execute('SELECT COUNT(*) FROM products')
    product_total = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM feedback')
    feedback_total = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM sale_order')
    purchase_total = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM sale_transaction')
    sale_total = cursor.fetchone()[0]

    conn.close()

    # Render the dashboard with totals
    return render_template(
        'dashboard.html', 
        product_total=product_total, 
        feedback_total=feedback_total, 
        purchase_total=purchase_total, 
        sale_total=sale_total
    )

@app.route('/feedback', methods=['POST'])
def feedback(): 
    if request.method == 'POST':
        name = request.form['fname']
        email = request.form['email']
        phone = request.form['phone']
        msg = request.form['msg']

        # Connect to MySQL and insert the data
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO feedback (name, email, phone, message) VALUES (%s, %s, %s, %s)", (name, email, phone, msg))
        conn.commit()  # Save changes to the database
        conn.close()

        flash('Customer Feedback successfully!', 'success')
        return redirect('/')

@app.route('/feedback_details')
def feedback_details():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM feedback ORDER BY id DESC")
    feedbacks = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'feedbackdetails.html',
        feedbacks=feedbacks
    )

@app.route('/customer_login')
def customer_login():
    return render_template('Customerlogin.html')

@app.route('/index_page')
def index_page():
    return render_template('index.html')

@app.route('/Custloginquery', methods=['GET', 'POST'])
def Custloginquery():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['psw']

        # Connect to MySQL and check customer credentials
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM custreg WHERE custEmail = %s AND custPass = %s",
            (username, password)
        )
        customer = cursor.fetchone()
        conn.close()

        if customer:
            session['customer_id'] = customer['cust_id']  # Store customer ID in session
            session['Customer_Mobile'] = customer['Customer_Mobile']
            flash('Login successful!', 'success')
            return redirect(url_for('sales'))  # Redirect to product page
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('customer_login'))

@app.route('/CustRegquery', methods=['POST'])
def CustRegquery():
    if request.method == 'POST':
        email = request.form['email']
        mobile = request.form['mobile']
        psw = request.form['psw']
        pswrepeat = request.form['pswrepeat']

        # Connect to MySQL and insert the data
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO custreg (custEmail, custPass, custRepass, Customer_Mobile) VALUES (%s, %s, %s, %s)",
            (email, psw, pswrepeat, mobile)
        )
        conn.commit()  # Save changes to the database
        conn.close()

        # Flash success message
        flash('Customer registered successfully!', 'success')

        # Redirect to the homepage or another route
        return redirect(url_for('customer_login'))

# change password for customer
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        email = request.form['email']  # Get email from the form
        old_password = request.form['field1']
        new_password = request.form['field2']
        confirm_password = request.form['field3']

        if new_password != confirm_password:
            flash("New password and confirm password do not match.")
            return redirect(url_for('/change_password'))

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Verify the old password for the given email
        cursor.execute("SELECT custPass FROM custreg WHERE custEmail = %s", (email,))
        user = cursor.fetchone()

        if user and user['custPass'] == old_password:
            # Update the password
            cursor.execute(
                "UPDATE custreg SET custPass = %s, custRepass = %s WHERE custEmail = %s",
                (new_password, confirm_password, email)
            )
            conn.commit()
            flash("Password changed successfully!")
            return redirect(url_for('customer_login'))  # Redirect to login page
        else:
            flash("Invalid email or old password.")

        cursor.close()
        conn.close()

    return render_template('change_password.html')

# end of code



# here Add Product 

# Route for product page
@app.route('/product_page', methods=['GET', 'POST'])
def product_page():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    product_id = request.args.get('product_id')
    if product_id:  # Search by Product ID
        cursor.execute('SELECT * FROM products WHERE product_id = %s', (product_id,))
    else:  # Fetch all products
        cursor.execute('SELECT * FROM products')
    
    products = cursor.fetchall()
    conn.close()
    return render_template('product.html', products=products, search_id=product_id)

# Route for adding a product
@app.route('/addproduct', methods=['POST'])
def add_product():
    product_data = {
        'product_type': request.form['productType'],
        'product_name': request.form['productName'],
        'product_desc': request.form['productDesc'],
        'product_image': request.files['productImage'],  # For file uploads
        'product_qty': request.form['productQuantity'],
        'product_rate': request.form['productRate'],
        'product_amt': float(request.form['productQuantity']) * float(request.form['productRate'])
    }

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO products (product_type, product_name, product_desc, product_image, product_qty, product_rate, product_amt) VALUES (%s, %s, %s, %s, %s, %s, %s)',
        (
            product_data['product_type'], 
            product_data['product_name'], 
            product_data['product_desc'], 
            product_data['product_image'].filename, 
            product_data['product_qty'], 
            product_data['product_rate'], 
            product_data['product_amt']
        )
    )
    conn.commit()
    conn.close()

    # Save image to folder
    product_data['product_image'].save(f'./static/Product/{product_data["product_image"].filename}')

    return redirect(url_for('product_page'))


# edit product
@app.route('/editproduct/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    # Fetch the product details from the database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # If the form is submitted via POST, update the product
    if request.method == 'POST':
        product_name = request.form['product_name']
        product_desc = request.form['product_desc']
        product_qty = float(request.form['product_qty'])
        product_rate = float(request.form['product_rate'])
        # product_amt = request.form['product_amt']
        product_amt = product_qty * product_rate
        
        # Update the product in the database
        update_query = """
        UPDATE products 
        SET product_name=%s, product_desc=%s, product_qty=%s, product_rate=%s,product_amt=%s
        WHERE product_id=%s
        """
        cursor.execute(update_query, (product_name, product_desc, product_qty, product_rate,product_amt, product_id))
        conn.commit()
        conn.close()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('product_page'))

    # Fetch the product details to prefill the form
    cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()
    conn.close()
    
    if not product:
        flash('Product not found!', 'danger')
        return redirect(url_for('product_page'))

    return render_template('edit_product.html', product=product)

# delete product

@app.route('/deleteproduct/<int:product_id>')
def deleteproduct(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
    conn.commit()
    conn.close()

    flash('Product deleted successfully!', 'success')
    return redirect(url_for('product_page'))

# end of add product 

# purchase data

# Home page (purchase page)
@app.route('/purchases', methods=['GET', 'POST'])
def purchases():
    if request.method == 'POST':
        product_id = request.form['product_id']
        product_name = request.form['product_name']
        product_rate = request.form['product_rate']
        quantity = 1  # Default quantity

        # Initialize cart session
        if 'cart' not in session:
            session['cart'] = []

        # Check if item exists in the cart
        cart = session['cart']
        product_names = [item['product_name'] for item in cart]
        if product_name in product_names:
            return "<script>alert('Item Already Exists');window.location.href='/purchases';</script>"
            # flash("Item already exists in the cart!", "info")
        else:
            cart.append({'product_name': product_name, 'product_rate': product_rate, 'quantity': quantity})
            session['cart'] = cart
            return "<script>alert('Item Added Successfully');window.location.href='/purchases';</script>"
            # flash("Item added to cart!", "success")
        return redirect(url_for('purchases'))

    # Display products
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT product_id, product_name, product_image, product_rate FROM products")
    products = cursor.fetchall()  # Fetch all products
    conn.close()

    if not products:
        flash('No products available!', 'warning')
    
    return render_template('purchase.html', products=products)


@app.route('/purchase_order_confirmation')
def purchase_order_confirmation():
    if 'order_confirmation' in session:
        return render_template('PurchaseConfirmation.html', order=session['order_confirmation'])
    return redirect('/cart_supplier')

# end of purchase data

# logout code for admin
@app.route('/logout')
def logout():
    # Clear the session
    session.clear()  # This removes all items in the session
    return render_template('index.html')  # Redirect to the login page (or home page)

# Home page (sale page)
@app.route('/sales', methods=['GET', 'POST'])
def sales():
    if request.method == 'POST':
        product_id = request.form['product_id']
        product_name = request.form['product_name']
        product_rate = request.form['product_rate']
        quantity = 1  # Default quantity

        # Initialize cart session
        if 'cart1' not in session:
            session['cart1'] = []

        # Check if item exists in the cart
        cart1 = session['cart1']
        product_names = [items['product_name'] for items in cart1]
        if product_name in product_names:
            return "<script>alert('Item Already Exists');window.location.href='/sales';</script>"
            # flash("Item already exists in the cart!", "info")
        else:
            cart1.append({'product_name': product_name, 'product_rate': product_rate, 'quantity': quantity})
            session['cart1'] = cart1
            return "<script>alert('Item Added Successfully');window.location.href='/sales';</script>"
            # flash("Item added to cart!", "success")
        return redirect(url_for('sales'))

    # Display products
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT product_id, product_name, product_image, product_rate FROM products")
    Products = cursor.fetchall()  # Fetch all products
    conn.close()

    if not Products:
        flash('No products available!', 'warning')
    
    return render_template('Saleproduct.html', Products=Products)

# Cart Page
@app.route('/CustomerCart', methods=['GET', 'POST'])
def CustomerCart():
    if request.method == 'POST':
        if 'Remove_Item' in request.form:
            product_name = request.form['product_name']
            cart1 = session.get('cart1', [])
            session['cart1'] = [items for items in cart1 if items['product_name'] != product_name]
            flash("Item removed from the cart!", "warning")
        elif 'Mod_Quantity' in request.form:
            product_name = request.form['product_name']
            new_quantity = int(request.form['Mod_Quantity'])
            for items in session.get('cart1', []):
                if items['product_name'] == product_name:
                    items['quantity'] = new_quantity
            flash("Quantity updated!", "success")
        return redirect(url_for('CustomerCart'))

    cart1 = session.get('cart1', [])
    return render_template('cart_customer.html', cart1=cart1)

@app.route('/clear_cart1')
def clear_cart1():
    session.pop('cart1', None)
    flash("Cart cleared!", "info")
    return redirect(url_for('sales'))

@app.route('/cart_customer', methods=['GET', 'POST'])
def cart_customer():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        try:
            # Get form data
            customer_name = request.form['customerName']
            customer_mobile = request.form['customerMobile']
            customer_address = request.form['customerAddress']
            gtotal = request.form['gtotal']
            pay_mode = request.form['pay_mode']
            bill_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get the current date and time

            # Insert into `sale_transaction`
            delivery_code = generate_code()
            cursor.execute("""
                INSERT INTO sale_transaction 
                (bill_date,Customer_Name, Customer_Mobile, Customer_Address, Grand_Total, Pay_Mode,delivery_code,order_status)
                VALUES (%s,%s, %s, %s, %s, %s, %s, %s)
            """, (bill_date,customer_name, customer_mobile, customer_address, gtotal, pay_mode, delivery_code, 'Pending'))
            conn.commit()
            session['Customer_Mobile'] = customer_mobile
            bill_no = cursor.lastrowid

            # Insert into `sale_order` using session data (cart)
            if 'cart1' in session:
                Cart_items = session['cart1']
                for items in Cart_items:
                    try:
                        # Insert into `sale_order`
                        cursor.execute("""
                            INSERT INTO sale_order (bill_no, Product_Name, Product_Price, Product_Qty)
                            VALUES (%s, %s, %s, %s)
                        """, (bill_no, items['product_name'], items['product_rate'], items['quantity']))
                        conn.commit()

                        # Update product stock in `products` table
                        cursor.execute("""
                            UPDATE products 
                            SET product_qty = product_qty - %s 
                            WHERE product_name = %s
                        """, (items['quantity'], items['product_name']))
                        conn.commit()

                    except Exception as e:
                        flash(f"Error processing cart item: {str(e)}")
                        conn.rollback()
                        return redirect('/cart_customer')
            else:
                flash("Cart is empty. Please add items to the cart.")
                return redirect('/cart_customer')

            # Store order confirmation details in session
            session['Order_confirmation'] = {
                'bill_no': bill_no,
                'customerName': customer_name,
                'customerMobile': customer_mobile,
                'customerAddress': customer_address,
                'gtotal': gtotal,
                'pay_mode': pay_mode,
                'bill_date':bill_date,
                'delivery_code': delivery_code,
                'order_status': 'Pending',
                'sale_details': Cart_items
            }

            # Clear cart
            session.pop('cart1', None)

            # Redirect to confirmation page
            return redirect('/customer_order_confirmation')

        except Exception as e:
            flash(f"An error occurred: {str(e)}")
            conn.rollback()
            return redirect('/cart_customer')

        finally:
            cursor.close()
            conn.close()

    # Render purchase form
    return render_template('cart_customer.html')

@app.route('/my_orders')
def my_orders():
    mobile = session.get('Customer_Mobile')

    if not mobile:
        return "No orders found"

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get only that customer's bills
    cursor.execute("SELECT * FROM sale_transaction WHERE Customer_Mobile=%s", (mobile,))
    cust_result = cursor.fetchall()

    orders = []
    for cust in cust_result:
        cursor.execute("SELECT * FROM sale_order WHERE bill_no=%s", (cust['bill_no'],))
        order_items = cursor.fetchall()

        orders.append({
            'bill_date': cust['bill_date'],
            'bill_no': cust['bill_no'],
            'delivery_code': cust['delivery_code'],
            'Grand_Total': cust['Grand_Total'],
            'order_status': cust['order_status'],
            'order_details': order_items
        })

    conn.close()

    return render_template('Myorders.html', orders=orders)

@app.route('/cancel_order/<int:bill_no>')
def cancel_order(bill_no):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT order_status FROM sale_transaction WHERE bill_no=%s",
        (bill_no,)
    )
    order = cursor.fetchone()

    if order['order_status'] == 'Delivered':
        flash("Delivered order cannot be cancelled")
        return redirect('/my_orders')

    cursor.execute("""
        UPDATE sale_transaction
        SET order_status='Order Cancelled'
        WHERE bill_no=%s
    """, (bill_no,))

    conn.commit()
    conn.close()

    flash("Order Cancelled Successfully")
    return redirect('/my_orders')

@app.route('/update_order_status/<int:bill_no>', methods=['POST'])
def update_order_status(bill_no):

    status = request.form['status']
    entered_code = request.form['delivery_code']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 🔹 Step 1: Get original delivery code
    cursor.execute("SELECT delivery_code FROM sale_transaction WHERE bill_no=%s", (bill_no,))
    data = cursor.fetchone()
    

    original_code = data['delivery_code']

    # 🔴 Step 2: Check only for Delivered
    if status == "Delivered":
        if entered_code != original_code:
            flash("Invalid Delivery Code ❌")
            return redirect('/customer_order_details')

    # ✅ Step 3: Update
    cursor.execute("""
    UPDATE sale_transaction
    SET order_status=%s
    WHERE bill_no=%s
    """, (status, bill_no))

    conn.commit()
    conn.close()

    return redirect('/customer_order_details')

@app.route('/invoice/<int:bill_no>')
def invoice(bill_no):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get bill info
    cursor.execute("SELECT * FROM sale_transaction WHERE bill_no=%s", (bill_no,))
    bill = cursor.fetchone()

    # Get items
    cursor.execute("SELECT * FROM sale_order WHERE bill_no=%s", (bill_no,))
    items = cursor.fetchall()

    conn.close()

    return render_template('CustomerConfirmation.html', bill=bill, orders=items)

@app.route('/customer_order_confirmation')
def customer_order_confirmation():

    if 'Order_confirmation' in session:
        return render_template('CustomerConfirmation.html', orders=session['Order_confirmation'])
    return redirect('/cart_customer')

# end of customer pages

# end of code for customer
@app.route('/Logout')
def Logout():
    # Clear the session
    session.clear()  # This removes all items in the session
    return render_template('index.html')  # Redirect to the login page (or home page)

# customer order details
@app.route('/customer_order_details')
def customer_order_details():
   
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch data for customer transactions
    cursor.execute("SELECT * FROM sale_transaction")
    cust_result = cursor.fetchall()

    # Prepare data for rendering
    orders = []
    for cust in cust_result:
        cursor.execute("SELECT * FROM sale_order WHERE bill_no = %s", (cust['bill_no'],))
        order_result = cursor.fetchall()

        orders.append({
            'bill_date': cust['bill_date'],
            'bill_no': cust['bill_no'],
            'Customer_Name': cust['Customer_Name'],
            'Customer_Mobile': cust['Customer_Mobile'],
            'Customer_Address': cust['Customer_Address'],
            'Grand_Total':cust['Grand_Total'],
            'Pay_Mode': cust['Pay_Mode'],
            'order_status': cust['order_status'],
            'order_details': order_result
        })

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Render the HTML template with the fetched data
    return render_template('CustomerOrderDetails.html', orders=orders,)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

