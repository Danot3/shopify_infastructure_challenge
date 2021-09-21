from flask import Flask, render_template
import sqlite3 as sql

app = Flask(__name__)

def get_cursor():
    conn = sql.connect("database.db")
    cur = conn.cursor()
    return (cur, conn)


def initialize_db():
    (cur, conn) = get_cursor()

    # Create products table with data
    cur.execute("DROP TABLE IF EXISTS products")
    cur.execute("CREATE TABLE products (name TEXT, imgpath TEXT)")
    cur.execute("""INSERT INTO products (name, imgpath) VALUES \
        ('Black Hoodie', 'images/black_hoodie.jpg'), \
        ('Black Tee Shirt', 'images/black_tee_shirt.jpg'), \
        ('Black Jeans', 'images/black_jeans.jpg'), \
        ('White Sneakers', 'images/white_sneakers.jpg')""")
    conn.commit()
    

@app.route("/")
def home_page():
    (cur, _) = get_cursor()
    cur.execute("SELECT rowid, * FROM products")
    
    rows = cur.fetchall()
    print("Retrieved %d database entries" % len(rows))
    
    # Pre-process product info for HTML templates
    products = []
    for row in rows:
        products.append({
            "id":    row[0],
            "name":  row[1],
            "src":   "/static/%s" % (row[2]),
        })
    return render_template("index.html", products=products)
 
if __name__ == '__main__':
    initialize_db()
    app.run(debug = True)