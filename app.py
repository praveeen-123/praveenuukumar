from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)


# =====================================================
# MYSQL SETTINGS
# =====================================================

DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "demo"


# =====================================================
# MYSQL CONNECTION
# =====================================================

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )


# =====================================================
# CREATE DATABASE / TABLE
# =====================================================

def init_db():

    # Connect without selecting database
    connection = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        charset="utf8mb4"
    )

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`"
            )

    finally:
        connection.close()

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS donations (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100),
                    email VARCHAR(150),
                    phone VARCHAR(30),
                    food VARCHAR(255),
                    quantity VARCHAR(100),
                    address TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

        connection.commit()

    finally:
        connection.close()


# =====================================================
# INDEX / STARTING PAGE
# =====================================================

@app.route("/")
def index():
    return render_template("index.html")


# =====================================================
# HOME
# =====================================================

@app.route("/home")
def home():
    return render_template("home.html")


# =====================================================
# ABOUT
# =====================================================

@app.route("/about")
def about():
    return render_template("about.html")


# =====================================================
# CONTACT
# =====================================================

@app.route("/contact")
def contact():
    return render_template("contact.html")


# =====================================================
# PROFILE
# =====================================================

@app.route("/profile")
def profile():
    return render_template("profile.html")


# =====================================================
# DONATE FOOD
# =====================================================

@app.route("/donate", methods=["GET", "POST"])
def donate():

    if request.method == "POST":

        name = request.form.get("name", "")
        email = request.form.get("email", "")
        phone = request.form.get("phone", "")
        food = request.form.get("food", "")
        quantity = request.form.get("quantity", "")
        address = request.form.get("address", "")

        connection = get_connection()

        try:

            with connection.cursor() as cursor:

                cursor.execute("""
                    INSERT INTO donations
                    (name, email, phone, food, quantity, address)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    name,
                    email,
                    phone,
                    food,
                    quantity,
                    address
                ))

            connection.commit()

        finally:
            connection.close()

        return redirect(url_for("home"))

    return render_template("donate.html")


# =====================================================
# RUN FLASK
# =====================================================

if __name__ == "__main__":

    init_db()

    print("")
    print("========================================")
    print("      FOOD DONATE FLASK PROJECT")
    print("========================================")
    print("MySQL : Connected")
    print("Flask : http://127.0.0.1:5000")
    print("========================================")
    print("")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )