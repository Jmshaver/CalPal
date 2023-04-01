from flask import Flask
from flask import render_template
import flask
import json
# from main import get_current_user
from calpal import CalPal
app = Flask(__name__)

# print("Starting")
# user_id = get_current_user()
user_id = 1
calpal = CalPal(user_id)
@app.route("/")
def get_index():
    return render_template('index.html')

@app.route("/api/", methods=["POST"])
def api():
    text = flask.request.get_json()['value']
    intent = calpal.get_intent(text.lower())

    calpal.handle_intent(intent, text.lower())
    return json.dumps({"response":text})