'''
Configuration and methods for sending mails.
'''
import smtplib
from email.mime.text import MIMEText

username = "username"
password = "password"
replyto = "reply@example.com"

def sendmail(to, subject, text):
    """
    Send an email.

    to      -- the email address to send the mail to
    subject -- the subject line to use
    text    -- the text to send
    """
    server = smtplib.SMTP('smtp.gmail.com:587')  
    server.starttls()  
    server.login(username,password)  

    to = safe_unicode(to)
    subject = safe_unicode(subject)
    text = safe_unicode(text)

    msg = MIMEText(text.encode("UTF-8"), "plain", "UTF-8")
    msg["Subject"] = subject
    msg["To"] = to
    msg["Reply-to"] = replyto

    server.sendmail(msg["Reply-to"], msg["To"], msg.as_string())
    
    server.quit() 

def safe_unicode(textstring):
    """ Returns a unicode representation of the given string. """
    try:
        return unicode(textstring, "UTF-8")
    except TypeError:
        return textstring #was already unicode
