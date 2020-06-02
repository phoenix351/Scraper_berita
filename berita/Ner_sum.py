from NER_processing import get_summary
import mysql.connector as MySQLdb
from Database_connection import Database_connection
from datetime import datetime,timedelta

db = Database_connection()
connection = db.connection
cursor = db.cursor
tanggal = (datetime.now()-timedelta(1)).strftime('%Y-%m-%d')
query = "SELECT * FROM `ner_tmp`"
cursor.execute(query)
list_res = cursor.fetchall()

list_person = get_summary([row[1] for row in list_res],'tokoh',tanggal)
list_organization = get_summary([row[2] for row in list_res],'organisasi',tanggal)
list_position = get_summary([row[3] for row in list_res],'posisi',tanggal)
list_indicator = get_summary([row[4] for row in list_res],'indikator',tanggal)
list_location = get_summary([row[5] for row in list_res],'lokasi',tanggal)
list_quote = get_summary([row[6] for row in list_res],'kutipan',tanggal)

semua_list_tuple = []
semua_list_tuple.extend(list_person)
semua_list_tuple.extend(list_organization)
semua_list_tuple.extend(list_indicator)
semua_list_tuple.extend(list_position)
semua_list_tuple.extend(list_location)
semua_list_tuple.extend(list_quote)
#insert ke database 	
query_insert = "INSERT INTO `ner_table` (tanggal,jenis,nama,jumlah), VALUES (%s,%s,%s,%s)"

cursor.executemany(sql, val)

connection.commit()

print(cursor.rowcount, "was inserted.")
