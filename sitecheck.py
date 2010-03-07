#!/usr/bin/env python

import sys, os, urllib2, smtplib, shutil, re, difflib, ConfigParser
from email.mime.text import MIMEText
from time import strftime
from BeautifulSoup import BeautifulSoup
from fileupdater import absUrl

VERSION = "1.4"

CONFFILES = []
CONFFILES.append(os.path.expanduser("~/.sitecheck.conf"))
CONFFILES.append(os.path.expanduser("~/.sitecheck-cred.conf"))
CONFFILES.append("sitecheck.conf")
CONFFILES.append("sitecheck-logins.conf")
CONFFILES.append("sitecheck-mail.conf")
CONFFILES.append("sitecheck-sites.conf")
CONFFILES.append("sitecheck-to.conf")

def main():
    config = ConfigParser.ConfigParser()
    config.read(CONFFILES)

    try:
        sites = getSites(config)
    except:
        return 1

    try:
        for site in sites:
            site.writeNew()
    except:
        return 1

    sitesWithDiff = [s for s in sites if s.hasDiff()]
    try:
        mail(sitesWithDiff)
    except:
        return 1

    for site in sites:
        site.move()

    return 0

def getSites(config):
    sites = []
    standardto = dict(config.items("to"))
    for section in config.sections():
        if section[:4] == "site":
            name = section[6:-1]
            if config.has_option(section, "to"):
                recipients = config.get(section, "to")
                to = [standardto[r] for r in recipients]
            else:
                to = standardto.values()
            for option in config.options(section):
                if option[:5] == "page.":
                    url = config.get(section, option)
                    sites.append(Site(name, option, url, to))
    return sites

def mail(sites):
    for site in sites:
        print site.getDiff()

def sendmail(to, subject, text):
    """
    Send an email.

    to      -- the email address to send the mail to
    subject -- the subject line to use
    text    -- the text to send
    """
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login("username","password")

    to = safe_unicode(to)
    subject = safe_unicode(subject)
    text = safe_unicode(text)

    msg = MIMEText(text.encode("UTF-8"), "plain", "UTF-8")
    msg["Subject"] = subject
    msg["To"] = to
    msg["Reply-to"] = "replyto"

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
    subject = "Observer Report - %s %s" % (sitenames, strftime("%Y-%m-%d"))

    body = "Observed Changes:\n"
    for site in sitesWithDiff:
        title = "%s %s - %s %s" % ("~"*10, site[0].name, "~"*10, site[0].url)
        body += "%s\n%s\n\n" % (title, site[1])
    body += "SiteCheck.py - " + VERSION

    return subject, body

class Site():
    def __init__(self, name, option, url, to):
        self.name = name
        self.oldfile = "%s-%s.old.txt" % (name, option[5:])
        self.newfile = "%s-%s.new.txt" % (name, option[5:])
        self.url = url
        self.to = to
        self.newlines = None
        self.diff = None

    def writeNew(self):
        newlines = self.getNewLines()
        file = open(self.newfile, "w")
        file.write("\n".join(newlines))
        file.close()

    def getNewLines(self):
        if self.newlines is None:
            rawcontent = urllib2.urlopen(self.url).read()
            newcontent = BeautifulSoup(rawcontent).prettify()
            self.newlines = newcontent.split("\n")
        return self.newlines

    def hasDiff(self):
        diff = self.getDiff()
        return diff is not None and 0 < len(diff)

    def getDiff(self):
        if self.diff is None:
            oldlines = self.getOldLines()
            if oldlines is not None:
                diff = difflib.ndiff(oldlines, self.getNewLines())
                self.diff = "\n".join([l for l in diff
                                       if not l.startswith("  ") and \
                                          not l.startswith("? ")])
            regexp = r'(?<=href=")[a-z0-9/]*\.pdf(?=")'
            matches = re.findall(regexp, self.diff)
            replaces = [(g, " %s " % absUrl(self.url, g)) for g in matches]
            for rep in replaces:
                self.diff = self.diff.replace(rep[0], rep[1])
        return self.diff

    def getOldLines(self):
        if os.path.exists(self.oldfile):
            file = open(self.oldfile, "r")
            content = file.read()
            file.close()
            return content.split("\n")
        else:
            return None

    def move(self):
        shutil.move(self.newfile, self.oldfile)

if __name__ == "__main__":
    sys.exit(main())
