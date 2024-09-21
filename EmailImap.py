import email
import imaplib
import os
from email.header import decode_header
import time
from Herramientas.Email import Email

class EmailImap(Email):
    def __init__(self, user, password, imapServer, imapPort):
        self._user = user
        self._password = password
        self._nameImapServer = imapServer
        self._portImap = imapPort
        self._imappserver = None
        

    def open(self):
        self._imapserver = imaplib.IMAP4_SSL(self._nameImapServer, self._portImap)
        self._imapserver.login(self._user, self._password)
        self.isOpenedImap = False

    
    def downloadAttachmentsInEmailByType(self, idMessage, outputDir, fileTypes, sinCode = False):
    
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
                            current_timestamp = time.time()
                            filename = part.get_filename().replace('/', '-')
                            if sinCode:
                                code= "_"+str(current_timestamp)+type

                                try:
                                    filename = filename.replace(type, code)
                                    open(os.path.join(outputDir, filename), 'wb').write(part.get_payload(decode=True))
                                except:
                                    filename, encoding = decode_header(part.get_filename())[0]
                                    filename = filename.decode('iso-8859-1')
                                    filename = filename.replace(type, code)
                                    open(os.path.join(outputDir, filename), 'wb').write(part.get_payload(decode=True))
                                    
                                filenames.append(part.get_filename().replace(type, code))
                                
                            
                            else:
                                try:
                                    open(os.path.join(outputDir, filename), 'wb').write(part.get_payload(decode=True))
                                except:
                                    filename, encoding = decode_header(part.get_filename())[0]
                                    filename = filename.decode('iso-8859-1')
                                    open(os.path.join(outputDir, filename), 'wb').write(part.get_payload(decode=True))

                                filenames.append(part.get_filename())
        return filenames
    
 
        