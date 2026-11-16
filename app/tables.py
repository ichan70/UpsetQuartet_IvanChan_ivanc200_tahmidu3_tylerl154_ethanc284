import sqlite3
import os
import time
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def setup():
    DB_FILE = "database.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS pages (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, text TEXT, creator_id INTEGER, created_at INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS page_history (edit_id INTEGER PRIMARY KEY AUTOINCREMENT, id INTEGER, last_editor_id INTEGER, last_update INTEGER, text TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS contributions (id INTEGER PRIMARY KEY AUTOINCREMENT, page_id INTEGER, contributor_id INTEGER, text TEXT, added_at INTEGER, FOREIGN KEY (page_id) REFERENCES pages(id), FOREIGN KEY (contributor_id) REFERENCES users(id))")

    # Insert the user "UpsetQuartet" if they don't already exist
    c.execute("SELECT id FROM users WHERE username = 'UpsetQuartet'")
    user_id_upset_quartet = c.fetchone()
    if not user_id_upset_quartet:
        c.execute("INSERT INTO users (username, password) VALUES ('UpsetQuartet', 'password')")
        user_id_upset_quartet = c.lastrowid
    else:
        user_id_upset_quartet = user_id_upset_quartet[0]

    # Insert the user "UpsetQuartetButCooler" if they don't already exist
    c.execute("SELECT id FROM users WHERE username = 'UpsetQuartetButCooler'")
    user_id_upset_quartet_but_cooler = c.fetchone()
    if not user_id_upset_quartet_but_cooler:
        c.execute("INSERT INTO users (username, password) VALUES ('UpsetQuartetButCooler', 'password')")
        user_id_upset_quartet_but_cooler = c.lastrowid
    else:
        user_id_upset_quartet_but_cooler = user_id_upset_quartet_but_cooler[0]

    # Insert stories into the database if they haven't been inserted already
    story_dir = os.path.join(BASE_DIR, "stories")
    for filename in os.listdir(story_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(story_dir, filename), 'r') as file:
                content = file.read()
                title_match = re.search(r'Title: (.+)', content)
                created_at_match = re.search(r'Created At: (.+)', content)
                if title_match and created_at_match:
                    title = title_match.group(1)
                    created_at = created_at_match.group(1)
                    parts = content.split('\n\n', 1)
                    if len(parts) > 1:
                        story_content = parts[1].strip()
                    else:
                        story_content = ""
                    insert_story(c, title, story_content, user_id_upset_quartet, created_at)
    db.commit()
    db.close()

def insert_story(c, title, text, creator_id, created_at):
    c.execute("SELECT id FROM pages WHERE title = ?", (title,))
    page = c.fetchone()
    if not page:
        c.execute("INSERT INTO pages (title, text, creator_id, created_at) VALUES (?, ?, ?, ?)",(title, text, creator_id, created_at))
        page_id = c.lastrowid
        c.execute("INSERT INTO page_history (id, last_editor_id, last_update, text) VALUES (?, ?, ?, ?)",(page_id, creator_id, created_at, text))
    else:
        page_id = page[0]
        c.execute("UPDATE pages SET text = ? WHERE id = ?",(text, page_id))
