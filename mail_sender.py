import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

import Configurations


class MailSender():

    def __init__(self, username=Configurations.mail_username, password=Configurations.mail_password,
                 mail_server=Configurations.mail_server):
        self.username = username
        self.password = password
        self.mail_server = mail_server
        self.msg = MIMEMultipart()

    def send_mail(self, to_email: str, subject: str, msg_body: str, image: MIMEImage = None):
        self.msg['From'] = self.username
        self.msg['To'] = to_email
        self.msg['Subject'] = subject
        self.msg.attach(MIMEText(msg_body))

        self.mail_server.ehlo()
        self.mail_server.login(self.username, self.password)
        self.mail_server.sendmail(self.username, to_email, self.msg.as_string())
        self.mail_server.quit()

