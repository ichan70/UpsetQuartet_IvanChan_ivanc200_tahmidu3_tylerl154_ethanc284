# The Upset Quartet
# Sep 10, 2026
# Project 00: Move Slowly and Fix Things
# 2026-11-18

import os
from flask import Flask, render_template, request, url_for, redirect, session
app = Flask(__name__)
# Insert secret key here.

@app.route("/")
def root():
        return redirect(url_for("login"))

@app.route("/login")
def login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password")
    
    return render_template("login.html")

@app.route("/signup")
def register():
    username = request.form.get("username", "").strip()
    password = request.form.get("password")
    otherPassword = request.form.get("otherPassword")
    
    return render_template("register.html")
    

if __name__ == "__main__":
    app.debug = True
    app.run()