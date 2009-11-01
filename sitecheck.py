'''
Checks a list of urls for changes.

See README for more information.
'''
import urllib, urllib2, cookielib
from time import strftime
from difflib import ndiff
from BeautifulSoup import BeautifulSoup

import sendmail, model

VERSION = "1.4"

siteslogedin = []
logins = model.getLogins()
tobesaved = []

jar = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(jar)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)

def checkSites():
    """ Start the site checking business. """

    
    recipients = dict([(r.name, r) for r in model.getRecipients()])
    sites = model.getSites()
    for site in sites:
        site.run()
        if site.mail != None:
            for recipient in site.to:
                recipients[recipient].sitesWithDiff.append(site)
    print "Found " + str(sum([1 for s in sites if s.mail != None])) + " Sites with diffs"
    
    mails = [constructEmail(r) for r in recipients.values() if 0 < len(r.sitesWithDiff)]
    if 0 < len(mails):
        sendmail.sendmail(mails, model.getMaillogindata())
    
    for site in tobesaved:
        model.put(site)

def checkSiteDiff(site):
    """ Download the site and diff it with the old version (if available). """
    if site.login != None:
        login(site.login)
    
    newcontent = getNormalizedContent(site)
    newlines = newcontent.split("\n")
    
    diff = None
    if not site.content == None and 0 < len(site.content.strip()):
        oldlines = site.content.split("\n")
        diff = "\n".join([line for line in ndiff(oldlines, newlines) if not line.startswith("  ") and not line.startswith("? ")])
    
    if site.content == None or 0 == len(site.content.strip()) or 0 < len(diff.strip()):
        site.content = newcontent
        tobesaved.append(site)
    
    return diff

def login(name):
    """ Performs a log in if not allready loged in. """
    if name not in siteslogedin:
        for login in logins:
            if login.name == name:
                for url in login.urls:
                    if len(url) == 1:
                        postData = None
                    else:
                        postData = dict([x.split("=") for x in url[1:]])
                    login = getResponse(url[0], postData).read()
                siteslogedin.append(name)

def getNormalizedContent(site):
    rawcontent = getResponse(site.url, None).read()
	prettycontent = BeautifulSoup(rawcontent).prettify()
    unicodecontent = sendmail.safe_unicode(prettycontent)
    content = unicode.encode('ascii', 'ignore')
    if site.regex != None:
        for regex in site.regex:
            content = re.sub(regex, '', content)
	return content

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

def constructEmail(recipient):
    """ Construct the subject and body for the Email. """
    subject = "Observer Report - "
    subject += ", ".join([site.name for site in recipient.sitesWithDiff])
    subject += " " + strftime("%d.%m.%Y")
    
    body = "Observed Changes:\n"
    for site in recipient.sitesWithDiff:
        body += "~"*10 + " " + site.name + " - " + site.url
        body += " " + "~"*10 + "\n"
        body += site.mail
        body += "\n\n"
    body += "SiteCheck.py - " + VERSION
    
    return (recipient.mail, subject, body)

if __name__ == "__main__":
    checkSites()

