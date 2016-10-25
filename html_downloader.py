# coding:utf8
import urllib2

class HtmlDownloader(object):

  def download(self,new_url):
    if new_url is None or len(new_url)==0:
      return None
    request=urllib2.Request(new_url)
    response=urllib2.urlopen(new_url)
    if response.getcode()!=200:
      return None
    return response.read()
