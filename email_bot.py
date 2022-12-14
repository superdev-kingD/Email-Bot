import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
import csv

port = 587  # For starttls
smtp_server = "smtp.gmail.com"

# Type your email and password
username = 'nemanja.radotic001@gmail.com'
# password is created by setting app password in google account
password = 'kqosndzhvorvcbpk'
subject = input('Please enter subject:')
message = input('Please enter message content:')
# input your email address
sender = "nemanja.radotic001@gmail.com"
# attached file
file_location = 'file.txt'

msg = MIMEMultipart()
msg['From'] = sender
msg['Subject'] = subject

msg.attach(MIMEText(message, 'plain'))

# Setup the attachment
filename = os.path.basename(file_location)
attachment = open(file_location, "rb")
part = MIMEBase('application', 'octet-stream')
part.set_payload(attachment.read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

# Attach the attachment to the MIMEMultipart object
msg.attach(part)
text = msg.as_string()

# Login to SMTP mail server
context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.connect('smtp.gmail.com', '587')
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted   
    server.login(username, password)
    
    with open("emails.csv") as file:
            reader = csv.reader(file)
            next(reader)  # it skips the header row
            for name, email in reader:
                msg['To'] = email
                server.sendmail(sender, email, text)
                
            
print('Message sent successfully')