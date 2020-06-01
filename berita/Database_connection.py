import mysql.connector as MySQLdb
class Database_connection:

	host = '192.168.43.7'
	user = 'root'
	password = '1234'
	db = 'phoenix'

	def __init__(self,tanggal='',*args,**kwargs):
		self.connection = MySQLdb.connect(
	            host=self.host,
	            user=self.user,
	            passwd=self.password,
	            database=self.db
	        )
		self.cursor = self.connection.cursor()