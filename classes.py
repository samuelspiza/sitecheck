'''
Classes
'''

class Site():
    def __init__(self, name, url, login, recipient):
        self.name = name
        self.url = url
        self.login = login
        self.recipient = recipient

class Login():
    def __init__(self, name, urls):
        self.name = name
        self.urls = urls

class Recipient():
    def __init__(self, name, mail):
        self.name = name
        self.mail = mail
        self.sitesWithDiff = []
