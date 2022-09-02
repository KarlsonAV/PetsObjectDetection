from flask import Flask, render_template
from views import do_hello_world


app = Flask(__name__)

@app.route("/")
def hello_world():
    return do_hello_world()