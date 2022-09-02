from flask import render_template


def do_hello_world():
    return render_template("hello.html")