from NER_processing import get_summary
from NER_processing import kata2list
import mysql.connector as MySQLdb
from Database_connection import Database_connection
from datetime import datetime,timedelta
import ast
import sys
import numpy as np
from collections import Counter
import operator

def summary_kelas(kode_list_str):
  for row in kode_list_str:
  	print(type(row))
  	break
 
  list_of_list = [kata2list(row) for row in kode_list_str]
  
  kode_list = []
  for list_ in list_of_list:
    kode_list.extend(list_)
  
  list_ = dict(sorted(Counter(kode_list).items(), key=operator.itemgetter(1),reverse=True))
  #res = np.array([{'nama':('IND'+'%03d' % (i+1)),'nilai':0} for i in range(114)])
  res = np.array([[('IND'+'%03d' % (i+1)),0] for i in range(114)])
  
  for indeks,nilai in list_.items():
    try:
    	cocok = np.where(res[:,0]=='indeks')[0][0]
    	res[cocok,1] = nilai
    except IndexError:
    	continue
    

  
  return res

tanggal = (datetime.now()-timedelta(1)).strftime('%Y-%m-%d')

db = Database_connection()
connection = db.connection
cursor = db.cursor

query = "SELECT * FROM `ner_tmp`"
cursor.execute(query)
list_res = cursor.fetchall()

list_person = get_summary([row[1] for row in list_res],'tokoh',tanggal)
list_organization = get_summary([row[2] for row in list_res],'organisasi',tanggal)
list_position = get_summary([row[3] for row in list_res],'posisi',tanggal)
list_indicator = get_summary([row[4] for row in list_res],'indikator',tanggal)
list_indicator_ = [row[4] for row in list_res]
list_location = get_summary([row[5] for row in list_res],'lokasi',tanggal)
list_quote = get_summary([row[6] for row in list_res],'kutipan',tanggal)

sum_in = summary_kelas(list_indicator_)
sum_val = [(str(row[0]),tanggal,int(row[1])) for row in sum_in]
query = "INSERT INTO indikator (id,tanggal,jumlah) VALUES (%s,%s,%s)"

cursor.executemany(query, sum_val)
connection.commit()
print(cursor.rowcount, "was inserted.")
sys.exit("debugging")

semua_list_tuple = []
semua_list_tuple.extend(list_person)
semua_list_tuple.extend(list_organization)
semua_list_tuple.extend(list_indicator)
semua_list_tuple.extend(list_position)
semua_list_tuple.extend(list_location)
semua_list_tuple.extend(list_quote)
#insert ke database 	


query_insert = "INSERT INTO `ner_table` (tanggal,jenis,nama,jumlah) VALUES (%s,%s,%s,%s)"


cursor.execute(query_insert, semua_list_tuple)

connection.commit()

print(cursor.rowcount, "was inserted.")
