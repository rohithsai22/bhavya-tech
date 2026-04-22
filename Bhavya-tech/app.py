from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "bhavya_secret"

# ---------------- DATABASE ----------------
DB_PATH = os.path.join(os.getcwd(), "database.db")

def get_db():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            mobile TEXT,
            project_type TEXT,
            budget TEXT,
            message TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def save_to_db(name, email, mobile, project_type, budget, message):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO requests (name, email, mobile, project_type, budget, message) VALUES (?, ?, ?, ?, ?, ?)",
            (name, email, mobile, project_type, budget, message)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print("DB Error:", e)

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/services")
def services():
    return render_template("service.html")

@app.route("/mobile")
def mobile():
    return render_template("mobile.html")

@app.route("/python")
def python_page():
    return render_template("python.html")

@app.route("/software")
def software():
    return render_template("software.html")

@app.route("/website")
def website():
    return render_template("website.html")

# ---------------- REQUEST ----------------
@app.route("/request", methods=["GET", "POST"])
def request_page():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        mobile = request.form.get("mobile")
        project_type = request.form.get("project_type")
        budget = request.form.get("budget")
        message = request.form.get("message")

        save_to_db(name, email, mobile, project_type, budget, message)

        return render_template("thankyou.html")

    return render_template("request.html")

# ---------------- ADMIN ----------------
admin_username = "bhavya"
admin_password = "83418"

@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/admin-login")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM requests ORDER BY id DESC")
    data = cur.fetchall()
    conn.close()

    return render_template("admin.html", data=data)

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == admin_username and password == admin_password:
            session["admin"] = True
            return redirect("/admin")
        else:
            return "Invalid Username or Password"

    return render_template("admin_login.html")

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)