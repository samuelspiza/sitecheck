'''
Checks a list of urls for changes.

See README for more information.
'''
import sys
from time import strftime
import urllib2
from difflib import ndiff
from BeautifulSoup import BeautifulSoup

import sendmail
import model

VERSION = "1.4"

def checkSites():
    """ Start the site checking business. """

    print 'Content-Type: text/plain'
    print ''
    
    sites = model.getSites()
    
    sitesWithDiff = []
    for site in sites:
        diff = checkSiteDiff(site)
        if diff is not None and 0 < len(diff.strip()):
            sitesWithDiff.append((site, diff.strip()))

    print "Found",len(sitesWithDiff), "Sites with diffs"

    if 0 < len(sitesWithDiff):
        subject, body = constructEmail(sitesWithDiff)

        print subject
        print body

        # Send the mail to every address in mails.txt
        recipients = model.getMails()
        sendmail.sendmail(recipients, subject, body)

def checkSiteDiff(site):
    """
    Download the site and diff it with the old version when it was downloaded
    before.

    site -- the site object

    return: result of the diff
    """

    rawcontent = urllib2.urlopen(site.url).read()
    newcontent = BeautifulSoup(rawcontent).prettify()
    newlines = newcontent.split("\n")
    
    diff = None
    if not site.content == None and 0 < len(site.content.strip()):
        oldlines = site.content.split("\n")
        diff = "\n".join([line for line in ndiff(oldlines, newlines) if not line.startswith("  ") and not line.startswith("? ")])

    if site.content == None or 0 == len(site.content.strip()) or 0 < len(diff.strip()):
        site.content = newcontent
        model.put(site)
    
    return diff

def constructEmail(sitesWithDiff):
        """ Construct the subject and body for the Email. """
        subject = "Observer Report - "
        subject += ", ".join([site[0].name for site in sitesWithDiff])
        subject += " " + strftime("%d.%m.%Y")
        
        body = "Observed Changes:\n"
        for site in sitesWithDiff:
            body += "~"*10 + " " + site[0].name + " - " + site[0].url
            body += " " + "~"*10 + "\n"
            body += site[1]
            body += "\n\n"
        body += "SiteCheck.py - " + VERSION
        
        return subject, body

if __name__ == "__main__":
    checkSites()

