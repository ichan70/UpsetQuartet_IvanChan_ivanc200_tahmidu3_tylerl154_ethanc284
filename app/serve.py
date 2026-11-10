"""
    Sticks & Feathers
    Tahmid Uddin, Charles Wu, Zhong Li Rui
    Software Development
    October 21, 2026
 """

from flask import Flask
from flask import session
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import os
import csv

app=Flask(__name__)
app.secret_key = "Ya-ha-ha! You found me!" #cookie encoding
csvFile = os.path.join("data", "users.csv")

def get_users(): #retrieves username and password
    users = {}
    if os.path.exists(csvFile): #i made my own csv and for some reason it wasn't playing nice, stackoverflow said to js use path.exists instead
        with open(csvFile, mode = "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2: #jic there's only a username and no password for some reason
                    users[row[0]] = row[1]
    return users

def saveUser(username, password): #adds user info to the csv file
    if not os.path.exists("data"):
        os.makedirs("data") #b/c csv is being stored in a data folder, this check is needed to make sure that hte directory exists
    with open(csvFile, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([username, password])

@app.route("/")
def index(): #chekc if log in
    if "username" in session:
        return redirect(url_for("welcome"))
    else:
        return redirect(url_for("login"))

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/auth", methods=["POST"]) #forces post cuz it'd be redundant to write GET code if we aren't gonna use it
def auth(): #checks if user alr exists, if passwords match, and if user is registering
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    action = request.form.get("action") #have the buttons interact with code
    if not username or not password:
        return redirect(url_for("login"))

    users = get_users()

    if action == "Register": #check if username alr exists before registering
        if username in users:
            return redirect(url_for("login"))
        saveUser(username, password)
        session["username"] = username
        return redirect(url_for("welcome"))

    elif action == "Login":
        if username not in users: #no user exists
            return redirect(url_for("login"))
        if users[username] != password: #password mismatch
            return redirect(url_for("login"))
        session["username"] = username
        return redirect(url_for("welcome"))
    return redirect(url_for("login")) #general chekc if any other error thingies happen

@app.route("/welcome")
def welcome():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session.get("username")
    return render_template("response.html", username=username)

@app.route("/logout")
def logout():
    session.pop("username", None) #none is used as the default jic any edge case happens
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.debug = True
    app.run()
