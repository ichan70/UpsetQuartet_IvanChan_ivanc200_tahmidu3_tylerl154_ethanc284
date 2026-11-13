# The Upset Quartet
# Sep 10, 2026
# Project 00: Move Slowly and Fix Things
# 2026-11-18

import os
from flask import Flask, render_template, request, url_for, redirect, session
import sqlite3
import tables
import time

app = Flask(__name__)
app.secret_key = os.urandom(32)  # Generates a random secret key

DB_FILE = "database.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False) #idk maybe fixes the thread stuff
c = db.cursor()
tables.setup()

@app.route("/")
def root():
    if 'username' in session:
        return redirect(url_for("user_profile", username=session['username']))
    return redirect(url_for("login"))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username", "").strip()
        password = request.form.get("password")
        #checks if passwords match by searching the database for the pair
        try: #exceptions maybe fix it?
            c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = c.fetchone()
        except sqlite3.Error as e:
            return f"Database error: {e}"

        if user:
            session['username'] = user[1] #makes a session for the user
            return redirect(url_for("user_profile", username=user[1])) #redirectts to profile
        else:
            return "Invalid username or password"

    return render_template("login.html")

@app.route("/signup", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get("username", "").strip()
        password = request.form.get("password")
        otherPassword = request.form.get("otherPassword")

        if password != otherPassword: #check for passwords matching
            return "Passwords do not match"
        #check if username already exists
        try:
            c.execute("SELECT * FROM users WHERE username = ?", (username,))
            if c.fetchone():
                return "Username already taken"
        except sqlite3.Error as e:
            return f"Database error: {e}"

        #adds to database
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            db.commit()
        except sqlite3.Error as e:
            return f"Database error: {e}"

        #makes session and redirects to profile
        session['username'] = username
        return redirect(url_for("user_profile", username=username))

    return render_template("register.html")

@app.route("/user/<username>")
def user_profile(username):
    #check if no session exists for user or wrong session
    if 'username' not in session or session['username'] != username:
        return redirect(url_for("login"))

    try:
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
    except sqlite3.Error as e:
        return f"Database error: {e}"

    if not user:
        return "User not found"
    #searches all stories where the user has created them
    try:
        c.execute("SELECT * FROM pages WHERE creator_id = ?", (user[0],))
        pages = c.fetchall()
    except sqlite3.Error as e:
        return f"Database error: {e}"

    return render_template("response.html", username=username, pages=pages)

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for("login"))

@app.route("/edit", methods=['GET', 'POST']) #i rmbr tyler saying something abt not doing post so i js did both
def edit():
    if 'username' not in session: #check to make sure it's an existing username
        return redirect(url_for("login"))
    username = session['username']
    page_id = request.args.get('page_id') #grabs page id from edit.html template
    if page_id:
        try:
            c.execute("SELECT * FROM pages WHERE id = ?", (page_id,)) #grabs page_id from the database
            page = c.fetchone()
        except sqlite3.Error as e: #exception jic sqlite3 throws an error
            return f"Database error: {e}"
        if not page:
            return "Error 404: Page not found" #simple jic page doesn't exist
    else:
        page = None
    if request.method == 'POST': #same thing but if its post
        title = request.form.get("title", "").strip()
        text = request.form.get("text", "").strip()
        page_id = request.form.get("page_id", "").strip()
        if page_id:
            try:
                c.execute("UPDATE pages SET text = ? WHERE id = ?", (text, page_id)) #code for adding content
                db.commit()
            except sqlite3.Error as e:
                return f"Database error: {e}"
        else:
            try:
                c.execute("SELECT id FROM users WHERE username = ?", (username,))
                user_id = c.fetchone()[0] #code for creating content
                c.execute("INSERT INTO pages (title, text, creator_id, created_at) VALUES (?, ?, ?, ?)", (title, text, user_id, int(time.time())))
                db.commit()
            except sqlite3.Error as e:
                return f"Database error: {e}" #jic sqlite3 gets fussy
        return redirect(url_for("user_profile", username=username))
    return render_template("edit.html", page=page, username=username)

@app.route("/index")
def indexing():
	if 'username' not in session:
		return redirect(url_for("login"))
	return render_template("index.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
