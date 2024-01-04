from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        stock = request.form['stock']

        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_product.html')

@app.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, price FROM products WHERE id=?", (product_id,))
    product = cursor.fetchone()
    cursor.execute("INSERT INTO cart (name, price, quantity) VALUES (?, ?, 1)", product)
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cart")
    cart_items = cursor.fetchall()
    conn.close()
    return render_template('cart.html', cart_items=cart_items)

if __name__ == '__main__':
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS cart (id INTEGER PRIMARY KEY, name TEXT, price REAL, quantity INTEGER)''')
    conn.close()
    app.run(debug=True)
