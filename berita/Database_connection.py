import mysql.connector as MySQLdb
class Database_connection:

	host = '192.168.43.7'
	#host = 'localhost'
	user = 'root'
	#password = ''
	password = '1234'
	db = 'skripsi_db'

	def __init__(self,tanggal='',*args,**kwargs):
		self.koneksi = MySQLdb.connect(
	            host=self.host,
	            user=self.user,
	            passwd=self.password,
	            database=self.db
	        )
		self.kursor = self.koneksi.cursor()
	def tutup(self):
		self.koneksi.close()