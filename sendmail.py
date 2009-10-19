'''
Configuration and methods for sending mails.
'''

from google.appengine.api import mail

replyto = "reply@example.com"

def sendmail(to, subject, text):
    """
    Send an email.

    to      -- the email address to send the mail to
    subject -- the subject line to use
    text    -- the text to send
    """

    to = safe_unicode(to)
    subject = safe_unicode(subject)
    text = safe_unicode(text)

    mail.send_mail(replyto, to, subject, text) 

def safe_unicode(textstring):
    """ Return a unicode representation of the given string. """
    try:
        return unicode(textstring, "UTF-8")
    except TypeError:
        return textstring #was already unicode
