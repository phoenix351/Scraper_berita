import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def kirim_notif(scraper):
	mail_content = '''
	Hello Developer, 
	Telah terjadi Error pada Web Scraper, Silahkan Diperiksa. 
	Terima Kasih
	'''
	#The mail addresses and password
	sender_address = 'dunlud351@gmail.com'
	sender_pass = 'kuat123087'
	receiver_address = '16.9351@stis.ac.id'
	#Setup the MIME
	message = MIMEMultipart()
	message['From'] = sender_address
	message['To'] = receiver_address
	message['Subject'] = 'Pemberitahuan Gangguan Web Scraper : '+scraper   #The subject line
	#The body and the attachments for the mail
	message.attach(MIMEText(mail_content, 'plain'))
	#Create SMTP session for sending the mail
	try:
		session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
	except:
		print("gagal membuat sesi")
		return
	
	session.starttls() #enable security
	
	try:
		session.login(sender_address, sender_pass) #login with mail_id and password
	except Exception as ex:
		print("Login gagal")
		print(ex)
		return
	
	text = message.as_string()
	try:
		session.sendmail(sender_address, receiver_address, text)
	except:
		print("Gagal mengirim email")
		return
	session.quit()
	print('Mail Sent')
if __name__ == '__main__':
	kirim_notif("Kompas")