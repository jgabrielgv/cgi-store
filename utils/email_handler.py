#!/usr/bin/python3
"""Handles the email functions"""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#from email.MIMEImage import MIMEImage
import smtplib
import collections

import os
import sys
__SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
__SCRIPT_DIR = os.path.normpath(os.path.join(__SCRIPT_DIR, '..'))
if not __SCRIPT_DIR in sys.path:
    sys.path.append(__SCRIPT_DIR)

class SmtpClient(object):
    """Creates an stmp client to send emails"""
    #Code obtained from:
    #http://code.activestate.com/recipes/473810-send-an-html-email-with-embedded-image-and-plain-t/

    def __init__(self, email_from, email_to):
        self.email_from = email_from
        self.email_to = email_to
        self.template = MIMEMultipart('related')

    def build_registration_template(self):
        # Define these once; use them twice!
        #strFrom = 'from@example.com'
        #strTo = 'to@example.com'

        """
        Upper image

        Dear Juan Gabriel,

Thank you for registering at Vuforia's Developer Portal.

Your account has been created with the email address jgmezvargas@gmail.com.

Click the following link to complete your registration
https://developer.vuforia.com/user/confirm?e=jgmezvargas@gmail.com&t=nnJOJjrlFxmncJpSBqynIErodPrBZwooqpzEXOLJRTixAbmRxNuOGhMfWNCvuVyY

If you have any issues accessing the link above please copy and paste it directly in your browser.

Thank you,

The Vuforia Team
        """

        # Create the root message and fill in the from, to, and subject headers
        #self.template = MIMEMultipart('related')
        self.template['Subject'] = 'Confirmacion de registro en Amezon'
        self.template['From'] = self.email_from
        self.template['To'] = ','.join(self.email_to) if self.__is_list(self.email_to) \
         else self.email_to
        self.template.preamble = 'This is a multi-part message in MIME format.'

        # Encapsulate the plain and HTML versions of the message body in an
        # 'alternative' part, so message agents can decide which they want to display.
        msg_alternative = MIMEMultipart('alternative')
        self.template.attach(msg_alternative)

        msg_text = MIMEText('This is the alternative plain text message.')
        msg_alternative.attach(msg_text)

        # We reference the image in the IMG SRC attribute by the ID we give it below
        msg_text = MIMEText('<b>Some <i>HTML</i> text</b> and an image.<br><br>Nifty!', 'html')
        #msg_text = MIMEText('<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>Nifty!', 'html')
        msg_alternative.attach(msg_text)

        # This example assumes the image is in the current directory
        #fp = open('test.jpg', 'rb')
        #msgImage = MIMEImage(fp.read())
        #fp.close()

        # Define the image's ID as referenced above
        #msgImage.add_header('Content-ID', '<image1>')
        #self.template.attach(msgImage)

    def __is_list(self, obj):
        return isinstance(obj, collections.Sequence) and not isinstance(obj, basestring)

    def send_email(self):
        """Sends the email with the previous defined properties"""
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.login('user@email.com', 'pass')
        smtp.sendmail(self.email_to, self.email_to, self.template.as_string())
        smtp.quit()
