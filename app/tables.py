import sqlite3

DB_FILE = "database.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS pages (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, text TEXT, creator_id INTEGER, created_at INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS page_history (edit_id INTEGER PRIMARY KEY AUTOINCREMENT, id INTEGER, last_editor_id INTEGER, last_update INTEGER, text TEXT)")
db.commit()
