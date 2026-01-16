import sqlite3

# 1. Connect to the SQLite database (creates file if it doesn't exist)
connection = sqlite3.connect("users_events.db")

# 2. Create a cursor (this lets us run SQL commands)
cursor = connection.cursor()

# 3. Read the schema.sql file
with open("schema.sql", "r") as file:
    schema_sql = file.read()

# 4. Execute the SQL to create tables
cursor.executescript(schema_sql)

# 5. Save changes and close connection
connection.commit()
connection.close()

print("Database setup complete. Tables created successfully.")
