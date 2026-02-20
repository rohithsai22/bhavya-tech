from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = "bhavya_super_secret_key"


# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            mobile TEXT,
            message TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()


def save_to_db(name, email, mobile, message):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO requests (name, email, mobile, message) VALUES (?, ?, ?, ?)",
        (name, email, mobile, message)
    )
    conn.commit()
    conn.close()


# ---------------- EMAIL FUNCTION ----------------
def send_email(name, email, mobile, message):
    try:
        EMAIL_USER = os.environ.get("EMAIL_USER")
        EMAIL_PASS = os.environ.get("EMAIL_PASS")

        if not EMAIL_USER or not EMAIL_PASS:
            print("Email environment variables not set!")
            return

        msg = EmailMessage()
        msg["Subject"] = "New Request - Bhavya Tech"
        msg["From"] = EMAIL_USER
        msg["To"] = EMAIL_USER

        msg.set_content(f"""
New Client Request

Name: {name}
Email: {email}
Mobile: {mobile}
Message: {message}
""")

        # ✅ Add timeout here (VERY IMPORTANT)
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()

        print("Email sent successfully!")

    except Exception as e:
        print("Email sending failed:", e)
        
# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/mobile")
def mobile():
    return render_template("mobile.html")


@app.route("/python")
def python_service():
    return render_template("python.html")


@app.route("/software")
def software():
    return render_template("software.html")


@app.route("/website")
def website():
    return render_template("website.html")


# ---------------- REQUEST FORM ----------------
@app.route("/request", methods=["GET", "POST"])
def request_page():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        mobile = request.form.get("mobile")
        message = request.form.get("message")

        save_to_db(name, email, mobile, message)
        send_email(name, email, mobile, message)

        return render_template("thankyou.html")

    return render_template("request.html")


# ---------------- ADMIN ----------------
admin_username = "admin"
admin_password = "88851"


@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/admin-login")

    conn = sqlite3.connect("database.db")
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