'''
Objects and functions for datastorage.
'''

import settings

def getSites():
    """
    Reads  available old versions, then returns a list of 'Site' Objects. 
    """
    return settings.sites

def getLogins():
    """ Returns a list of 'Login' Objects. """
    return settings.logins

def getRecipients():
    """ Returns a list of 'Recipient' Objects. """
    return settings.recipients

def getMaillogindata():
    """ Returns a list of 'Login' Objects. """
    return settings.maillogindata

def put(site):
    """ Save the new content of a site in a file. """
    file = open(site.name + ".old", "w")
    file.write(site.content)
    file.close()
