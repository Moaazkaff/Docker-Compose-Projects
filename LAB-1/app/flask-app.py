# claude new version

import os
import time
import mysql.connector
from mysql.connector import Error
from flask import Flask, jsonify

app = Flask(__name__)

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.environ.get("MYSQL_HOST", "localhost"),
            user=os.environ.get("MYSQL_USER"),
            password=os.environ.get("MYSQL_PASSWORD"),
            database=os.environ.get("MYSQL_DATABASE")
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def wait_for_db(retries=10, delay=3):
    """MySQL may not be ready immediately when the container starts."""
    for attempt in range(retries):
        conn = get_db_connection()
        if conn and conn.is_connected():
            print("Successfully connected to the database.")
            conn.close()
            return True
        print(f"DB not ready, retrying ({attempt + 1}/{retries})...")
        time.sleep(delay)
    return False


@app.route("/")
def index():
    return jsonify({"message": "Flask app is running!"})


@app.route("/db-test")
def db_test():
    conn = get_db_connection()
    if conn and conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify({"status": "connected", "database": db_name[0]})
    return jsonify({"status": "error", "message": "Could not connect to database"}), 500


if __name__ == "__main__":
    wait_for_db()
    app.run(host="0.0.0.0", port=5000, debug=False)

# # gemini

# from flask import Flask, render_template

# # Initialize the Flask application
# app = Flask(__name__)

# # Define the main route (the homepage)
# @app.route('/')
# def home():
#     # This will render the index.html file from your templates folder
#     return render_template('index.html', title="My Flask Web Page")

# if __name__ == '__main__':
#     # host='0.0.0.0' tells Flask to accept external connections
#     app.run(host='0.0.0.0', port=5000)

# claud

# from flask import Flask, render_template

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return render_template("index.html")

# if __name__ == '__main__':
#     # host='0.0.0.0' tells Flask to accept external connections
#     app.run(host='0.0.0.0', port=5000)


