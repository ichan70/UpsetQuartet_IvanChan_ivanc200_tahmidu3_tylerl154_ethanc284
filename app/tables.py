import sqlite3
import csv

DB_FILE = "database.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()

#remove table if it already exists
c.execute("DROP TABLE IF EXISTS users")
c.execute("DROP TABLE IF EXISTS pages")
c.execute("DROP TABLE IF EXISTS edits")

#creates tables
userTable = "CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT)"
pageTable = "CREATE TABLE pages (id INTEGER PRIMARY KEY, creator_id INTEGER, created_at INTEGER, title STRING, text STRING)"
editTable = "CREATE TABLE edits (edit_id INTEGER PRIMARY KEY, story_id INTEGER, last_editor_id INTEGER, edited_at INTEGER, text STRING)"

c.execute(userTable);
c.execute(pageTable);
c.execute(editTable);

#adds values into tables
c.execute("INSERT INTO users VALUES (?, ?)", (Username, Password))
c.execute("INSERT INTO pages VALUES (?, ?, ?, ?, ?)", (ID, Creator_ID, Created_at, Title, Text))
c.execute("INSERT INTO pages VALUES (?, ?, ?, ?, ?)", (Edit_ID, Story_ID, Last_Editor_ID, Edited_at, Text))

db.commit()
db.close()