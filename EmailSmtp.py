
import smtplib
from Herramientas.Email import Email

class EmailSmtp(Email):
    
    def __init__(self, user, password, smtpServer, smptPort):
        self._user = user
        self._password = password

        self._nameSmtpServer = smtpServer
        self._portSmpt = smptPort
        self._smtpserver = None
        
        self._imappserver = None

    def open(self):
        self._smtpserver = smtplib.SMTP_SSL(self._nameSmtpServer, self._portSmpt)
        self._smtpserver.login(self._user, self._password)
   
