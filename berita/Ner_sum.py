from NER_processing import get_summary
import mysql.connector as MySQLdb

host = 'localhost'
user = 'root'
password = ''
db = 'phoenix'

connection = MySQLdb.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            database=self.db
        )
cursor = self.connection.cursor()

query = "SELECT * FROM ner_temp"
cursor.execute(query)
cursor.fetchall()
