
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

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == '__main__':
    # host='0.0.0.0' tells Flask to accept external connections
    app.run(host='0.0.0.0', port=5000)
