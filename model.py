import os

def getSites():
    siteFile = open("sites.txt", "r")
    sitesLines = siteFile.readlines()
    return processSitesInFile(sitesLines)

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

def getMails():
    return open("mails.txt", "r").readlines()

def getOld(site):
    if not os.path.exists(site + ".old"):
        return None
    else:
        file = open(site + ".old")
        oldlines = [line.rstrip() for line in file]
        file.close()
        return oldlines

def put(site, content):
    if os.path.exists(site + ".old"):
        os.remove(site + ".old")
    file = open(site + ".old", "w")
    file.write(content)
    file.close()
