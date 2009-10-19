'''
Checks a list of urls for changes.

See README for more information.
'''
import sys
from time import strftime

import sendmail
import sites
import model

VERSION = "1.4"

def checkSites():
    """ Start the site checking business. """

    siteDict = model.getSites()

    sitesWithDiff = {}
    for site in siteDict:
        diff = sites.checkSite(siteDict, site)
        if diff is not None:
            if len(diff.strip()) > 0:
                sitesWithDiff[site] = diff.strip()

    print "Found",len(sitesWithDiff), "Sites with diffs"

    # construct the email notice
    if len(sitesWithDiff) > 0:
        subject = "Observer Report - "
        text = "Observed Changes:\n"
        for site in sitesWithDiff:
            subject += site + ", "

            text += "~"*10 + " " + site + " - " + siteDict[site]
            text += " " + "~"*10 + "\n"
            text += sitesWithDiff[site]
            text += "\n\n"

        subject = subject[:-2]
        subject += " " + strftime("%d.%m.%Y")
        text += "SiteCheck.py - " + VERSION

        print subject
        print text

        # Send the mail to every address in mails.txt
        mails = model.getMails()

        for mail in mails:
            mail = mail.strip()
            if len(mail) > 0 and not mail.startswith("#"):
                sendmail.sendmail(mail, subject, text)

if __name__ == "__main__":
    try:
        sys.exit(checkSites())
    except Exception:
        print Exception # Stupid but gets the job done...
        sys.exit(1)

