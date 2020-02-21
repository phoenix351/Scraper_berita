import sqlite3
conn = sqlite3.connect('kompas.sqlite')
cursor = conn.cursor()
print("Opened database successfully")
