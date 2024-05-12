import sqlite3

# Connection to DB
connection = sqlite3.connect(database="instance/blog.db")

# Making Cursor
cursor = connection.cursor()

# Dropping the table
cursor.execute("DROP TABLE IF EXISTS Table_Name_Goes_Here")

cursor.close()