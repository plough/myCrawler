'''
Created on 2016-1-26

@author: Administrator
'''
import urllib2

class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return None
        response = urllib2.urlopen(url)
        if response.getcode() != 200:  # @UndefinedVariable
            return None
        return response.read()  # @UndefinedVariable





