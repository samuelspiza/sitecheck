import os
import sites
from google.appengine.ext import db

class Site(db.Model):
  name = db.StringProperty(required=True)
  content = db.StringProperty(multiline=True)

def getSites():
    return dict([("example","http://www.example.com/")])

def getMails():
    return ["to@example.com"]

def getOld(site):
    old = [seite for seite in db.GqlQuery("SELECT * FROM Site") if seite.name == site]
    print len(old)
    if len(old) == 0:
        print "blub"
        return None
    else:
        return old[-1].content.split("\n")

def put(site, content):
    old = [seite for seite in db.GqlQuery("SELECT * FROM Site") if seite.name == site]
    if len(old) == 0:
        s = Site(name=site)
    else:
        s = old[-1]
    s.content = content
    db.put(s)

