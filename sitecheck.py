#!/usr/bin/env python

__version__ = "1.4"

import sys, os, urllib2, smtplib, shutil, re, difflib, ConfigParser
from email.mime.text import MIMEText
from time import strftime
from BeautifulSoup import BeautifulSoup
from fileupdater import absUrl

CONF_FILES = [os.path.expanduser("~/.sitecheck.conf"),"sitecheck-logins.conf",
              os.path.expanduser("~/.sitecheck-cred.conf"),"sitecheck.conf",
              "sitecheck-to.conf","sitecheck-mail.conf","sitecheck-sites.conf"]

def main():
    config = ConfigParser.ConfigParser()
    config.read(CONF_FILES)

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
        mail(config, sitesWithDiff)
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
                to = [s.trim() for s in config.get(section, "to").split(",")]
            else:
                to = standardto.keys()
            for option in config.options(section):
                if option[:5] == "page.":
                    url = config.get(section, option)
                    sites.append(Site(name, option, url, to))
    return sites

def mail(config, sites):
    global MAIL_SERVER
    MAIL_SERVER = smtplib.SMTP(config.get("mail", "server"))
    if config.has_option("mail", "tls") and config.getboolean("mail", "tls"):
        MAIL_SERVER.starttls()
    username = config.get("mail", "username")
    password = config.get("mail", "password")
    MAIL_SERVER.login(username, password)
    
    replyto = config.get("mail", "replyto")
    to = config.items("to")
    for addressee in to:
        asites = [s for s in sites if addressee[0] in s.to]
        subject, body = constructEmail(asites)
        sendmail(addressee[1], replyto, subject, body)

    MAIL_SERVER.quit()

def sendmail(to, replyto, subject, body):
    """Send an email."""
    to = safe_unicode(to)
    subject = safe_unicode(subject)
    body = safe_unicode(body)

    print body
    
    msg = MIMEText(body.encode("UTF-8"), "plain", "UTF-8")
    msg["Subject"] = subject
    msg["To"] = to
    msg["Reply-to"] = replyto

    MAIL_SERVER.sendmail(msg["Reply-to"], msg["To"], msg.as_string())

def safe_unicode(textstring):
    """Return a unicode representation of the given string."""
    try:
        return unicode(textstring, "UTF-8")
    except TypeError:
        return textstring #was already unicode

def constructEmail(sites):
    """Construct the subject and body for the Email."""
    sitenames = ", ".join([site.name for site in sites])
    subject = "Observer Report - %s %s" % (sitenames, strftime("%Y-%m-%d"))

    body = "Observed Changes:\n"
    for site in sites:
        title = "%s %s - %s %s" % ("~"*10, site.name, site.url, "~"*10)
        body += "%s\n%s\n\n" % (title, site.getDiff())
    body += "SiteCheck.py - " + __version__

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
            # make pdfs clickable
            reg = r'(?<=href=")[a-z0-9/\.]*\.pdf(?=")'
            rep = '(?<=href=")%s(?=")'
            m = re.findall(reg, self.diff)
            replaces = [(rep % g, " %s " % absUrl(self.url, g)) for g in m]
            for rep in replaces:
                self.diff = re.sub(rep[0], rep[1], self.diff)

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
