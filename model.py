'''
Configuration, objects and functions for datastorage and watched websites.
'''

from google.appengine.ext import db

class Site(db.Model):
    """ The GAE DB data object to save a cached version of a website. """
    name = db.StringProperty(required=True)
    url = db.StringProperty(required=True)
    content = db.StringProperty(multiline=True)

def getSites():
    """ Return a dict containing url of watched pages and their identifier. """
    sites = []
    sites.append(("example", "http://www.example.com/"))
    sites = dict(sites)
    objs = db.GqlQuery(db.GqlQuery("SELECT * FROM Employee WHERE name IN :1",
                                   sites))
    missing = [Site(name=it[0],url=it[1]) for it in sites.items() if it[0] not in [o.name for o in objs]]
    return objs + missing

def getMails():
    """ Return a list of recipients. """
    mails = []
    mails.append("to@example.com")
    return mails

def put(site):
    """ Update the cached version or create it in database. """
    db.put(site)
