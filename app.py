from flask import Flask, render_template, request
import sqlite3
import smtplib
from email.message import EmailMessage

app = Flask(__name__)


# ---------- DATABASE ----------
def save_to_db(name, email, mobile, message):
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
    cur.execute(
        "INSERT INTO requests (name, email, mobile, message) VALUES (?, ?, ?, ?)",
        (name, email, mobile, message)
    )
    conn.commit()
    conn.close()


# ---------- EMAIL ----------
def send_email(name, email, mobile, message):
    msg = EmailMessage()   # ✅ THIS is line ~20 (defined properly)

    msg.set_content(
        f"New Client Request\n\n"
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Mobile: {mobile}\n"
        f"Message: {message}"
    )

    import smtplib
from email.message import EmailMessage

def send_email(name, email, mobile, message):
    msg = EmailMessage()
    msg.set_content(
        f"New Client Request\n\n"
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Mobile: {mobile}\n"
        f"Message: {message}"
    )

    msg["Subject"] = "New Request - Bhavya Tech"
    msg["From"] = "rohithsai22@outlook.com"
    msg["To"] = "rohithsai22@outlook.com"

    server = smtplib.SMTP("smtp.office365.com", 587)
    server.starttls()
    server.login("rohithsai22@outlook.com", 
    "Bhavana@21")
    server.send_message(msg)
    server.quit()


# ---------- HOME ----------
@app.route("/")
def home():
    return render_template("index.html")


# ---------- REQUEST ----------
@app.route("/request", methods=["GET", "POST"])
def request_page():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        mobile = request.form.get("mobile")
        message = request.form.get("message")

        save_to_db(name, email, mobile, message)
        # send_email(name, email, mobile, message)

        return render_template("thankyou.html")

    return render_template("request.html")


# ---------- ADMIN ----------
@app.route("/admin")
def admin():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM requests")
    data = cur.fetchall()
    conn.close()
    return render_template("admin.html", data=data)


# ---------- RUN ----------
if __name__== "__main__":
     app.run()
            