'''
Compare the websites with the cached version and creating diff.
'''

import urllib2
import model
from difflib import ndiff

from BeautifulSoup import BeautifulSoup

def checkSite(siteDict, site):
    """
    Download the site and diff it with the old version when it was downloaded
    before.

    siteDict -- the dictionary of name->url
    site -- the name of the site as used in the siteDict

    return: result of the diff
    """

    diff = None
    url = siteDict[site]
    hash = url.__hash__()
    print url
    content = urllib2.urlopen(url).read()
    prettyContent = BeautifulSoup(content).prettify()
    newlines = prettyContent.split("\n")
    oldlines = model.getOld(site)
    if not oldlines == None:
        diff = "\n".join([line for line in ndiff(oldlines, newlines) if not line.startswith("  ") and not line.startswith("? ")])
    model.put(site, prettyContent)
    return diff
