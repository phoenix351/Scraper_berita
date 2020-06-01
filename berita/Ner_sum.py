from NER_processing import get_summary
import mysql.connector as MySQLdb
from Database_connection import Database_connection

db = Database_connection()
connection = db.connection
cursor = db.cursor

query = "SELECT * FROM ner_temp"
cursor.execute(query)
list_res = cursor.fetchall()
for row in list_res:
	print(row)
	
