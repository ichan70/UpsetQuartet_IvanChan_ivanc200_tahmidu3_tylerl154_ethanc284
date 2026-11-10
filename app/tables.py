import sqlite3
import csv

DB_FILE = "database.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()

c.execute("DROP TABLE IF EXISTS users")
command = "CREATE TABLE users (name TEXT PRIMARY KEY, password TEXT)"

c.execute(command)