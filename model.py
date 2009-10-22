'''
Configuration, objects and functions for datastorage and watched websites.
'''

from google.appengine.ext import db

class Site(db.Model):
    """ The GAE DB data object to save a cached version of a website. """
    name = db.StringProperty(required=True)
    url = db.StringProperty(required=True)
    content = db.TextProperty()

def getSites():
    """ Return a dict containing url of watched pages and their identifier. """
    return db.GqlQuery("SELECT * FROM Site")

def getMails():
    """ Return a list of recipients. """
    mails = []
    mails.append("%recipient%")
    return mails

def put(site):
    """ Update the cached version or create it in database. """
    db.put(site)
