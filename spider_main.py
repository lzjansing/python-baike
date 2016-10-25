# coding:utf8
from bs4 import BeautifulSoup

import url_manager
import html_parser
import html_downloader
import html_outputer

class SpiderMain(object):
  def __init__(self):
    self.urls=url_manager.UrlManager()
    self.downloader=html_downloader.HtmlDownloader()
    self.outputer=html_outputer.HtmlOutputer()
    self.parser=html_parser.HtmlParser(config)

  def craw(self,root_url):
    death_count=int(config.find('count').text)
    count=1
    self.urls.add_new_url(root_url)
    while self.urls.has_new_url():
      try:
        new_url=self.urls.get_new_url()
        print 'craw %d : %s' %(count,new_url)
        html_cont=self.downloader.download(new_url)
        new_urls,new_data=self.parser.parse(new_url,html_cont)
        self.urls.add_new_urls(new_urls)
        self.outputer.collect_data(new_data)
        if count>=death_count:
          break
        count=count+1
      except Exception,e:
        print 'craw failed:',e
    self.outputer.output_html()


if __name__=='__main__':
  try:
    config_file=open('config.xml','r')
    config=config_file.read()
  finally:
    config_file.close()
    config_file=None
  config=BeautifulSoup(config, 'lxml',from_encoding='utf-8')
  print 'begin'
  root_url=config.find('root-url').text
  obj_spider=SpiderMain()
  obj_spider.craw(root_url)

