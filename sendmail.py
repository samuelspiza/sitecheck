'''
Configuration and methods for sending mails.
'''

import smtplib
from email.mime.text import MIMEText

def sendmail(mails, maillogindata):
    """ Send the emails. """
    server = smtplib.SMTP(maillogindata["server"])
    if "tls" in maillogindata and maillogindata["tls"]:
        server.starttls()
    server.login(maillogindata["user"],maillogindata["pass"])
    for mail in mails:
        recipient = safe_unicode(mail[0])
        subject = safe_unicode(mail[1])
        text = safe_unicode(mail[2])
        msg = MIMEText(text.encode("UTF-8"), "plain", "UTF-8")
        msg["Subject"] = subject
        msg["To"] = recipient
        msg["Reply-to"] = maillogindata["replyto"]
     
        server.sendmail(msg["Reply-to"], msg["To"], msg.as_string())
    
    server.quit()
 
def safe_unicode(textstring):
    """ Return a unicode representation of the given string. """
    try:
        return unicode(textstring, "UTF-8")
    except TypeError:
        return textstring #was already unicode
