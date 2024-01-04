import sqlite3

# ایجاد یک اتصال به دیتابیس
conn = sqlite3.connect('products.db')
cursor = conn.cursor()

# ساخت جدول محصولات
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
)
''')

# ساخت جدول سبد خریدS
cursor.execute('''
CREATE TABLE IF NOT EXISTS cart (
    id INTEGER PRIMARY KEY,
    product_id INTEGER,
    FOREIGN KEY (product_id) REFERENCES products (id)
)
''')

# ذخیره تغییرات و بستن اتصال
conn.commit()
conn.close()
