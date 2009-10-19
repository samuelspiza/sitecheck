import os
import sites

def getSites():
    siteFile = open("sites.txt", "r")
    sitesLines = siteFile.readlines()
    return sites.processSitesInFile(sitesLines)

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
