'''
Used as a centralized way to send email over an SMTP server.
'''
import os
import urllib2
import shutil
import model
from difflib import ndiff

from BeautifulSoup import BeautifulSoup

def processSitesInFile(sitesLines):
    """
    Iterate over the lines from the sites.txt and create a
    dictionary that maps the sites' names to their url.

    sitesLines -- list of Strings directly taken from the file
    """

    sites = {}
    for site in sitesLines:
        site = site.strip()
        
        # Ignore lines starting with # as comments
        if site.startswith("#"):
            continue
        
        try:
            parts = site.split("=")
            if len(parts) == 2:
                sites[parts[0].strip()] = parts[1].strip()
            else:
                print "Unknown site format: {0}".format(site)
        except exception:
            print "Error: {0}".format(exception)
            
    return sites

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
