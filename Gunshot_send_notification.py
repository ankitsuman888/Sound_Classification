import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from twilio.rest import Client

def send_sms(type_of_class, phone, per):
    
    if (phone == 'NULL'):
        pass
    
    else:
        try:
            account = "ACf484b463a2bec8ae4dff8bdc2f9a74f5"
            token ="061b89b1789ca6b549c80d24f62dba1f"
            
            client = Client(account, token)
            
            t = "+91" + str(phone)
            f = "+17573849675"
            
            b = "\nThere is " +str(per)+ "% chance that we have detected : "+ str(type_of_class)
            
            client.messages.create(to = t, from_ = f, body = b)
        
        except:
            print("Check internet connection !")
            print("Number may not be registered. ")
            pass


def send_email(type_of_class, email, per):
    
    if (email == 'NULL'):
        pass
    
    else:    
        # Your email details
        fromaddr = "ankitsuman70@gmail.com"
        PASSWORD = "1234wwssxxcc"
        
        # Email message
        SUBJECT = "Sound Classification Service (by NCTC)"
        
        body = "\nThere is " +str(per)+ "% chance that we have detected : "+ str(type_of_class)
        
        toaddr = str(email)
        
        try:
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = SUBJECT
        
            msg.attach(MIMEText(body, 'plain'))
        
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(fromaddr, PASSWORD)
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            server.quit()
            print("Email sent to '" + toaddr + "' successfully!")
        
        except:
            print("Check internet connection !")
            pass

'''
import smtplib
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("ankitsuman70@gmail.com", "1234wwssxxcc")
 
msg = "YOUR MESSAGE!"
server.sendmail("ankitsuman70@gmail.com", "ankitsuman80@gmail.com", msg)
server.quit()
'''


'''
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
 
 
fromaddr = "YOUR ADDRESS"
toaddr = "ADDRESS YOU WANT TO SEND TO"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "SUBJECT OF THE MAIL"
 
body = "YOUR MESSAGE HERE"
msg.attach(MIMEText(body, 'plain'))
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "YOUR PASSWORD")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()

'''


'''
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
 
fromaddr = "YOUR EMAIL"
toaddr = "EMAIL ADDRESS YOU SEND TO"
 
msg = MIMEMultipart()
 
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "SUBJECT OF THE EMAIL"
 
body = "TEXT YOU WANT TO SEND"
 
msg.attach(MIMEText(body, 'plain'))
 
filename = "NAME OF THE FILE WITH ITS EXTENSION"
attachment = open("PATH OF THE FILE", "rb")
 
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 
msg.attach(part)
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "YOUR PASSWORD")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()

'''