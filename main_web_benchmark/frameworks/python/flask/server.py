import os
import uuid
from flask import Flask, jsonify, request
import pymysql

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "admin")
DB_PASS = os.getenv("DB_PASS", "secret")
DB_NAME = os.getenv("DB_NAME", "benchmark_db")

def get_db():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

@app.route("/", methods=["GET"])
def root():
    return jsonify({"status": "success", "language": "Python", "framework": "Flask", "port": 8011})

@app.route("/raw/1table", methods=["GET"])
def raw_1table():
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users LIMIT 100")
            return jsonify(cursor.fetchall())
    finally:
        conn.close()

@app.route("/raw/post/1table", methods=["POST"])
def post_1table():
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            random_id = str(uuid.uuid4())[:8]
            email = f"flask_{random_id}_{os.getpid()}@example.com"
            cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (f"User_{random_id}", email))
            return jsonify({"user_id": cursor.lastrowid}), 201
    finally:
        conn.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8011, threaded=True)
