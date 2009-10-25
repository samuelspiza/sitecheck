'''
Classes
'''

class Site():
    def __init__(self, name, url, to, login=None, regex=None):
        self.name = name
        self.url = url
        self.to = to
        self.login = login
        self.regex = regex

class Login():
    def __init__(self, name, urls):
        self.name = name
        self.urls = urls

class Recipient():
    def __init__(self, name, mail):
        self.name = name
        self.mail = mail
        self.sitesWithDiff = []
