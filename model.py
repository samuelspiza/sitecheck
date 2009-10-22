'''
Objects and functions for datastorage.
'''

import os

class Site():
    def __init__(self, name, url, login, recipient):
        self.name = name
        self.url = url
        self.login = login
        self.recipient = recipient

class Login():
    def __init__(self, name, urls):
        self.name = name
        self.urls = urls

class Recipient():
    def __init__(self, name, mail):
        self.name = name
        self.mail = mail

def getSites():
    """
    Reads the 'sites.conf' and available old versions, then returns a list of 
    'Site' Objects. 
    """
    file = open("sites.conf", "r")
    sites = parseSites([x for x in file.readlines() if 0 < len(x.strip()) and not x.strip().startswith("#")])
    file.close()
    for site in sites:
        readContent(site)
    return sites

def parseSites(lines):
    """ Parses each line from 'sites.conf' building a 'Site' object. """
    sites = []
    for line in lines:
        name, url, login, recipient = [x.strip() for x in line.split(";")]
        if login == "None":
            login = None
        sites.append(Site(name, url, login, recipient))
    return sites

def readContent(site):
    """ Reads the old version of a site from a file. """
    if not os.path.exists(site.name + ".old"):
        site.content = None
    else:
        file = open(site.name + ".old", "r")
        site.content = file.read()
        file.close()

def getLogins():
    """ Reads 'logins.conf' and returns a list of 'Login' Objects. """
    file = open("logins.conf", "r")
    logins = parseLogins([x for x in file.readlines() if 0 < len(x.strip()) and not x.strip().startswith("#")])
    file.close()
    return logins

def parseLogins(lines):
    """ Parses each line from 'logins.conf' building a 'Login' object. """
    logins = []
    for line in lines:
        name, urls = [x.strip() for x in line.split(";")]
        urls = urls.split("_,_")
        logins.append(Login(name, urls))
    return logins

def getRecipients():
    """ Reads 'recipients.conf' and returns a list of 'Recipient' Objects. """
    file = open("recipients.conf", "r")
    recipients = parseRecipients([x for x in file.readlines() if 0 < len(x.strip()) and not x.strip().startswith("#")])
    file.close()
    return recipients

def parseRecipients(lines):
    """
    Parses each line from 'recipients.conf' building a 'Recipients' object.
    """
    recipients = []
    for line in lines:
        name, mail = [x.strip() for x in line.split(";")]
        recipients.append(Recipient(name, mail))
    return recipients

def put(site):
    """ Save the new content of a side in a file. """
    file = open(site.name + ".old", "w")
    file.write(site.content)
    file.close()
