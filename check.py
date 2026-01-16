import os
import sqlite3

DB_NAME = "users_events.db"

print("Current working directory:", os.getcwd())
print("DB file exists here?:", os.path.exists(DB_NAME))
print("Absolute DB path:", os.path.abspath(DB_NAME))

conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM users;")
print("Users count:", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM events;")
print("Events count:", cur.fetchone()[0])

conn.close()
