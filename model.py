'''
Configuration, objects and functions for datastorage and watched websites.
'''

from google.appengine.ext import db

class Site(db.Model):
    """ The GAE DB data object to save a cached version of a website. """
    name = db.StringProperty(required=True)
    content = db.StringProperty(multiline=True)

def getSites():
    """ Return a dict containing url of watched pages and their identifier. """
    sites = []
    sites.append(("example", "http://www.example.com/"))
    return dict(sites)

def getMails():
    """ Return a list of recipients. """
    mails = []
    mails.append("to@example.com")
    return mails

def getOld(site):
    """Return a list of lines of a watched site cached at last execution 
	or 'None' if no cached version available.
	"""
    old = [s for s in db.GqlQuery("SELECT * FROM Site") if s.name == site]
    if len(old) == 0:
        return None
    else:
        return old[-1].content.split("\n")

def put(site, content):
    """ Update the cached version or create it in database. """
    old = [s for s in db.GqlQuery("SELECT * FROM Site") if s.name == site]
    if len(old) == 0:
        s = Site(name=site)
    else:
        s = old[-1]
    s.content = content
    db.put(s)

