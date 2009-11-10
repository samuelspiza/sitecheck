'''
Checks a list of urls for changes.

See README for more information.
'''
import sys, re
from time import strftime
import urllib, urllib2, cookielib
from difflib import ndiff
from BeautifulSoup import BeautifulSoup
from google.appengine.ext import db

import sendmail
import model

VERSION = "1.4"

jar = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(jar)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)

def checkSites():
    """ Start the site checking business. """

    postData = dict([("user", "%zimkennung%"),
                     ("pass", "%zimpassword%"),
                     ("submit", "Anmelden"),
                     ("pid", "1004"),
                     ("logintype", "login")])
    dummy = getResponse("http://www.pim.wiwi.uni-due.de/studium-lehre/lehrveranstaltungen/wintersemester-0910/opm-1518/", postData).read()

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

        recipients = model.getMails()
        sendmail.sendmail(recipients, subject, body)

def getResponse(url, postData = None):
    header = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
            'Accept-Language': 'de',
            'Accept-Encoding': 'utf-8'}
    if(postData is not None):
        postData = urllib.urlencode(postData)
    req = urllib2.Request(url, postData, header)
    try:
        return urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print 'Error Code:', e.code
        return None

def checkSiteDiff(site):
    """
    Download the site and diff it with the old version when it was downloaded
    before.

    site -- the site object

    return: result of the diff
    """
    replaces = [r'\?submit=Anmelden&amp;logintype=login&amp;pid=1004&amp;redirect_url=',
                r'\?submit=Abmelden&amp;logintype=logout&amp;pid=1004',
                r'\?logintype=login&amp;pid=1004&amp;submit=Anmelden']
    replaces2 = [u'\xfc', u'\xdc', u'\xe4', u'\xf6', u'\xdf', u'\u2212', u'\u2013', u'\u201e', u'\u201c', u'\u2026', u'\xc4']
    replaces.extend(replaces2)
    logins = ["OPM - Vorlesung", "OPM - Tutorium", "OPM - Uebung", "IuF - Vorlesung", "IuF - Uebung", "IuF - Tutorium", "FIBA - Downloads OPM"]
    postData = dict([("user", "%zimkennung%"),
                     ("pass", "%zimpassword%"),
                     ("submit", "Anmelden"),
                     ("pid", "1004"),
                     ("logintype", "login")])
    if site.name in logins:
        rawcontent = getResponse(site.url, postData)
    else:
        rawcontent = getResponse(site.url)
    newcontent = sendmail.safe_unicode(BeautifulSoup(rawcontent).prettify())
    for repl in replaces:
        newcontent = re.sub(repl, '', newcontent)
    newlines = newcontent.split("\n")

    diff = None
    if not site.content == None and 0 < len(site.content.strip()):
        oldlines = site.content.split("\n")
        diff = "\n".join([line for line in ndiff(oldlines, newlines) if not line.startswith("  ") and not line.startswith("? ")])

    if site.content == None or 0 == len(site.content.strip()) or 0 < len(diff.strip()):
        site.content = db.Text(newcontent)
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

