#!/usr/bin/env python

import sys, urllib2, smtplib, difflib, ConfigParser
from email.mime.text import MIMEText
from time import strftime
from BeautifulSoup import BeautifulSoup

VERSION = "1.4"

CONFFILES = []
CONFFILES.append(os.path.expanduser("~/.sitecheck.conf"))
CONFFILES.append(os.path.expanduser("~/.sitecheck-cred.conf"))
CONFFILES.append("sitecheck.conf")
CONFFILES.append("sitecheck-addresses.conf")
CONFFILES.append("sitecheck-mail.conf")
CONFFILES.append("sitecheck-logins.conf")
CONFFILES.append("sitecheck-sites.conf")

def main():
    try:
        sites = getSites()
    except:
        return 1

    try:
        for site in sites:
            site.writeNew()
    except:
        return 1

    sitesWithDiff = [s for s in sites if s.hasDiff()]
    try:
        sendMail(sitesWithDiff)
    except:
        return 1

    for site in sites:
        site.move()

    return 0

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
    """ Return a unicode representation of the given string. """
    try:
        return unicode(textstring, "UTF-8")
    except TypeError:
        return textstring #was already unicode

def constructEmail(sitesWithDiff):
    """ Construct the subject and body for the Email. """
    sitenames = ", ".join([site[0].name for site in sitesWithDiff])
    subject = "Observer Report - %s %s" % (sitenames, strftime("%d.%m.%Y"))

    body = "Observed Changes:\n"
    for site in sitesWithDiff:
        title = "%s %s - %s %s" % ("~"*10, site[0].name, "~"*10, site[0].url)
        body += "%s\n%s\n\n" % (title, site[1])
    body += "SiteCheck.py - " + VERSION

    return subject, body

class Site():
    def checkSiteDiff(self):
        """
        Download the site and diff it with the old version when it was
        downloaded before.
        """

        rawcontent = urllib2.urlopen(site.url).read()
        newcontent = BeautifulSoup(rawcontent).prettify()
        newlines = newcontent.split("\n")

        diff = None
        if not site.content == None:
            oldlines = site.content.split("\n")
            diff = "\n".join([l for l in difflib.ndiff(oldlines, newlines)
                              if not line.startswith("  ") and \
                                 not line.startswith("? ")])

        if site.content == None or 0 < len(diff.strip()):
            site.content = newcontent
            model.put(site)

        return diff

if __name__ = "__main__":
    sys.exit(main())
