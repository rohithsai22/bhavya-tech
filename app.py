from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
import smtplib
from email.message import EmailMessage
from openai import OpenAI

app = Flask(_name_)
app.secret_key = os.environ.get("SECRET_KEY", "bhavya_secret")

# ---------------- AI SETUP ----------------
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_website(user_input):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"""
Create a professional real-world website.

Requirements:
- Clean modern UI
- Looks like built by developer (not AI)
- Include navbar, hero, services, contact, footer
- Responsive design

Idea: {user_input}

Return only full HTML with internal CSS.
"""
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"<h2>Error generating website</h2><p>{e}</p>"


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


# ---------------- EMAIL ----------------
def send_email(name, email, mobile, message):
    try:
        EMAIL_USER = os.environ.get("EMAIL_USER")
        EMAIL_PASS = os.environ.get("EMAIL_PASS")

        if not EMAIL_USER or not EMAIL_PASS:
            print("❌ Email config missing")
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

        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()

        print("✅ Email sent")

    except Exception as e:
        print("❌ Email failed:", e)


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


# ---------------- AI BUILDER ----------------
@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        idea = request.form.get("idea")
        result = generate_website(idea)
        return render_template("result.html", code=result)

    return render_template("create.html")


# ---------------- REQUEST ----------------
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
admin_username = os.environ.get("ADMIN_USER", "admin")
admin_password = os.environ.get("ADMIN_PASS", "12345")


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
            return render_template("admin_login.html", error="Invalid credentials")

    return render_template("admin_login.html")


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")


# ---------------- RUN ----------------
if _name_ == "_main_":
    app.run(debug=True