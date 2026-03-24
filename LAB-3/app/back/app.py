from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import os

app = Flask(__name__)
CORS(app)

# ─────────────────────────────────────────
# DATABASE — reads from docker-compose env vars
# ─────────────────────────────────────────

def get_db():
    """Open a connection to PostgreSQL using environment variables."""
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST",     "db"),
        port=os.environ.get("DB_PORT",     5432),
        user=os.environ.get("DB_USER",     "example"),
        password=os.environ.get("DB_PASSWORD", "example"),
        dbname=os.environ.get("DB_NAME",   "example")
    )
    return conn


# ─────────────────────────────────────────
# ROUTES — API only (nginx serves the HTML)
# ─────────────────────────────────────────

@app.route("/users", methods=["GET"])
def get_users():
    """Return all users as JSON."""
    conn = get_db()
    cur  = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM users ORDER BY id")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([dict(u) for u in users]), 200


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """Return a single user by ID."""
    conn = get_db()
    cur  = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    row  = cur.fetchone()
    cur.close()
    conn.close()
    if row is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(dict(row)), 200


@app.route("/add-user", methods=["POST"])
def add_user():
    """Create a new user."""
    data = request.json

    if not data or not data.get("name") or not data.get("email"):
        return jsonify({"error": "name and email are required"}), 400

    name  = data["name"].strip()
    email = data["email"].strip()

    try:
        conn = get_db()
        cur  = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s)",
            (name, email)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "User created successfully"}), 201

    except psycopg2.errors.UniqueViolation:
        return jsonify({"error": "Email already exists"}), 409


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Delete a user by ID."""
    conn = get_db()
    cur  = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    deleted = cur.rowcount
    cur.close()
    conn.close()

    if deleted == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted"}), 200


# ─────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────

if __name__ == "__main__":
    print("Flask API running → http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)