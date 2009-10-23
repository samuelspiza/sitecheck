'''
Objects and functions for datastorage.
'''

import os
import settings

def getSites():
    """
    Reads  available old versions, then returns a list of 'Site' Objects. 
    """
    sites = settings.sites
    for site in sites:
        readContent(site)
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
    """ Returns a list of 'Login' Objects. """
    return settings.logins

def getRecipients():
    """ Returns a list of 'Recipient' Objects. """
    return settings.recipients

def put(site):
    """ Save the new content of a site in a file. """
    file = open(site.name + ".old", "w")
    file.write(site.content)
    file.close()
