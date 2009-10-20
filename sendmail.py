'''
Configuration and methods for sending mails.
'''

from google.appengine.api import mail

replyto = "reply@example.com"

def sendmail(recipients, subject, body):
    """
    Send an email.

    to      -- the email address to send the mail to
    subject -- the subject line to use
    body    -- the text to send
    """

    subject = safe_unicode(subject)
    body = safe_unicode(body)
    for to in recipients:
        to = safe_unicode(to)

        mail.send_mail(replyto, to, subject, body) 

def safe_unicode(textstring):
    """ Return a unicode representation of the given string. """
    try:
        return unicode(textstring, "UTF-8")
    except TypeError:
        return textstring #was already unicode
