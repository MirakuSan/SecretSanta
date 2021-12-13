from random import choice
import os
from os.path import basename
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import yaml
import hashlib

# import .yaml file for credentials (create it yourself!)
credentials = yaml.safe_load(open('./credentials.yml'))

smtp_server =  credentials['mail']['server']
sender_email = credentials['mail']['email']
password = credentials['mail']['password']
port = 587



donne=["me","you","him","her"] #list of people

Emailaddresses = { # Dict with name and email address
    "me": "Me@gmail.com",
    "you": "you@gmail.com",
    "him": "him@gmail.com",
    "her": "her@gmail.com"
}

subject = "🎅 Le Noël Secret"
text ="""\
Salut XXX !

Regarde la pièce jointe pour savoir à qui tu fais un cadeau 🎁👋

Maximum 15€ cette année !😱

Bisous
Toto 💖 """

recois = donne[:]
liste = [ [ None for y in range( 2 ) ] for x in range(0,len(donne) ) ]


def send_mail(email,file,mail_text):

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(mail_text))

    part = MIMEApplication(open(file, 'rb').read())
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file)
    msg.attach(part)

    smtp = smtplib.SMTP(smtp_server,port)
    smtp.starttls()
    smtp.login(sender_email,password)
	
    smtp.sendmail(sender_email, email, msg.as_string())
    print("mail sended to "+email)

    smtp.quit()

def picksomeone(recois) :
    for i in range(0, len(donne)):
        donne_name = donne[i]
        recois_name = choice(recois)
        liste[i][0] = donne_name
        liste[i][1] = recois_name
        recois.remove(recois_name)
    for i in range(0, len(liste)) :
        if liste[i][0] == liste[i][1] :
            print("Found same ... Reroll !")
            recois = donne[:]
            picksomeone(recois)

picksomeone(recois)
print("Hand verify with sha256 sums")

for i in  range(0, len(liste)):
    print (hashlib.sha256(liste[i][0].encode('utf-8')).hexdigest() + " offre à " + hashlib.sha256(liste[i][1].encode('utf-8')).hexdigest())

if not os.path.exists('people/'):
    os.makedirs('people/')

for i in range(0, len(liste)):
    with open(('people/' + liste[i][0] + '.txt'),'w',encoding='utf-8-sig') as f :
            f.write(liste[i][0] + " offre à " + liste[i][1])
    f.close()
    send_mail(Emailaddresses[liste[i][0]],os.path.abspath('people/' + liste[i][0] + '.txt'),text.replace("XXX",liste[i][0]))
	
print("Done !")