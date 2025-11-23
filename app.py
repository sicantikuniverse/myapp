from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Lokasi database (wajib absolute path untuk Vercel)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = db()
    rows = conn.execute("SELECT * FROM items").fetchall()
    conn.close()
    return render_template("index.html", rows=rows)

@app.route("/add", methods=["POST"])
def add():
    text = request.form["text"]
    conn = db()
    conn.execute("INSERT INTO items(text) VALUES (?)", (text,))
    conn.commit()
    conn.close()
    return redirect("/")

# Wajib untuk Vercel
def vercel_app():
    return app

app = vercel_app()

if __name__ == "__main__":
    app.run(debug=True)
