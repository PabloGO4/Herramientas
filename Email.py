import email
import imaplib
import os
import smtplib
from email import encoders
from email.header import decode_header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from loguru import logger

class Email:
    
    def __init__(self, user, password, smtpServer, smptPort, imapServer, imapPort):
        self._user = user
        self._password = password

        self._nameSmtpServer = smtpServer
        self._portSmpt = smptPort
        self._smtpserver = None
        
        self._nameImapServer = imapServer
        self._portImap = imapPort
        self._imappserver = None

    def open(self):
        self._smtpserver = smtplib.SMTP(self._nameSmtpServer, self._portSmpt)
        self._smtpserver.ehlo()
        self._smtpserver.starttls()
        self._smtpserver.ehlo()
        
        self._smtpserver.login(self._user, self._password)
        
        self._imapserver = imaplib.IMAP4_SSL(self._nameImapServer, self._portImap)
        self._imapserver.login(self._user, self._password)
        self.isOpenedImap = False

    @staticmethod
    def __createPartFile(pathFile):
        with open(pathFile, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        nameFile = os.path.basename(pathFile)
        nameFile = nameFile.replace('Ñ', 'N')
        nameFile = nameFile.replace('Ó', 'O')
        
        encoders.encode_base64(part)
        part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {nameFile}",
                )
        
        return part
    
    def sendMail(self, subject, contents, sendTo=[]):
        
        msg = MIMEMultipart('alternative')
        msg['subject'] = subject
        # msg['To'] = sendto
        msg['To'] = ", ".join(sendTo)
        msg['From'] = self._user
        msg.preamble = ""
 
        htmlBody = MIMEText(contents, 'html')
        msg.attach(htmlBody)        
 
        strInfo = f"Enviando a {sendTo}"
        logger.info(strInfo)

        self._smtpserver.sendmail(self._user, sendTo, msg.as_string())

    @staticmethod
    def __createPartFile(pathFile):
        with open(pathFile, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        nameFile = os.path.basename(pathFile)
        nameFile = nameFile.replace('Ñ', 'N')
        nameFile = nameFile.replace('Ó', 'O')
        
        encoders.encode_base64(part)
        part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {nameFile}",
                )
        
        return part
    
    def sendMailWithAttachment(self, subject, contents, sendTo=[], pathFileToAttach=[]):
        
        msg = MIMEMultipart('alternative')
        msg['subject'] = subject
        # msg['To'] = sendto
        msg['To'] = ", ".join(sendTo)
        msg['From'] = self._user
        msg.preamble = ""
 
        htmlBody = MIMEText(contents, 'html')
        msg.attach(htmlBody)

        if len(pathFileToAttach) > 1:
            for file in pathFileToAttach:
                partFile = Email.__createPartFile(file)
                msg.attach(partFile)
        else:
            partFile = Email.__createPartFile(pathFileToAttach[0])
            msg.attach(partFile)         
 
        strInfo = f"Enviando a {sendTo}"
        logger.info(strInfo)

        self._smtpserver.sendmail(self._user, sendTo, msg.as_string())



    def getIdsMailInBoxNotSeen(self):
        
        self.isOpenedImap = True
        self._imapserver.select('inbox')
        
        result, data = self._imapserver.uid('search', None, '(UNSEEN)')
        assert(result == 'OK')
        mailIds = data[0].split()
        
        return mailIds

    def getIdsMailInBoxBySender(self, sender):
            
        self.isOpenedImap = True
        self._imapserver.select('inbox')
        
        result, data = self._imapserver.uid('search', None, f'FROM {sender}')
        assert(result == 'OK')
        mailIds = data[0].split()
        
        return mailIds
    
    def getMessage(self, idMessage):
        result, data = self._imapserver.uid('fetch', idMessage, '(RFC822)' )
        assert(result == 'OK')
        
        msg = None
        
        for responsePart in data:
            if isinstance(responsePart,tuple):
                msg = email.message_from_bytes(responsePart[1])
                break
            
        assert(msg != None)
            
        return msg
        

    def getBodyMessage(self, msg):

        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))

                if ctype in ['text/plain', 'html/plain'] and 'attachment' not in cdispo:
                    body = part.get_payload(decode=True)
                    body = body.decode('Latin1', 'replace')
                    break

        else:
            body = msg.get_payload(decode=True)
            body = body.decode('utf-8', 'replace')

        return body
    

    def downloadAttachmentsInEmailByType(self, idMessage, outputDir, fileTypes):
    
        result, data = self._imapserver.uid('fetch', idMessage, '(RFC822)' )
        assert(result == 'OK')

        filenames = []
        emailBody = data[0][1]
        mail = email.message_from_bytes(emailBody)
        if mail.get_content_maintype() != 'multipart':
            return
        for part in mail.walk():
            if part.get_content_maintype() != 'multipart' and part.get('Content-Disposition') is not None:
                if 'attachment' in part.get('Content-Disposition'):
                    for type in fileTypes:
                        if type in part.get_filename():
                            filename = part.get_filename().replace('/', '-')
                            try:
                                open(os.path.join(outputDir, filename), 'wb').write(part.get_payload(decode=True))
                            except:
                                filename, encoding = decode_header(part.get_filename())[0]
                                filename = filename.decode('iso-8859-1')
                                open(os.path.join(outputDir, filename), 'wb').write(part.get_payload(decode=True))

                            filenames.append(part.get_filename())
        
        return filenames
    
    def getMessageHeader(self, idMessage):
        result, data = self._imapserver.uid('fetch', idMessage, '(RFC822)' )
        assert(result == 'OK')
        emailbody=data[0][1]
        mail = email.message_from_bytes(emailbody)
        return {
            'Subject': mail['Subject'],
            'from': mail['From'],
            'to': mail['To'],
            'Date': mail['Date']
            }
        
    def close(self, smtp=False, imap=False):
        if smtp and imap :
            self._smtpserver.quit()
            self._imapserver.shutdown()
            return
        if  smtp :
            self._smtpserver.quit()
            return
        if imap :
            self._imapserver.shutdown()
            return

