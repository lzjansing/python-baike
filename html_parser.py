from bs4 import BeautifulSoup
import urlparse
import re

class HtmlParser(object):
  def __init__(self,config):
    self.url_patterns=[]
    for url in config.find_all('url-pattern'):
      self.url_patterns.append(url.text)
    self.data_patterns=[]
    for data in config.find_all('data-pattern'):
      data_pattern={}
      data_pattern['title']=data.find('title').text
      find = data.find('find')
      find_conds=[]
      while find != None:
        find_cond = {}
        tag = find.find('tag')
        if tag != None:
          find_cond['tag'] = tag.text
        class_ = find.find('class')
        if class_ != None:
          find_cond['class'] = class_.text
        if len(find_cond) != 0:
          find_conds.append(find_cond)
        find = find.find('find')
      data_pattern['find_conds']=find_conds
      self.data_patterns.append(data_pattern)

  def _get_new_urls(self,page_url,soup):
    # /view/123.html
    new_full_urls=set()
    for url_pattern in self.url_patterns:
      links=soup.find_all('a',href=re.compile(r""+url_pattern))
      for link in links:
        new_url=link['href']
        new_full_url=urlparse.urljoin(page_url,new_url)
        new_full_urls.add(new_full_url)
    return new_full_urls

  def _get_new_data(self,page_url,soup):
    res_data={}

    res_data['url']=page_url
    for data_pattern in self.data_patterns:
      node=soup
      for find_cond in data_pattern['find_conds']:
        tag=find_cond.get('tag')
        tag_class=find_cond.get('class')
        if tag!=None and tag_class!=None:
          node=node.find(tag,tag_class)
        elif tag!=None:
          node=node.find(tag)
        elif tag_class!=None:
          node=node.find(class_=tag_class)
      res_data[data_pattern['title']]=node.get_text()
    return res_data


  def parse(self,page_url,html_cont):
    if page_url is None or html_cont is None:
      return
    soup=BeautifulSoup(html_cont, 'html.parser',from_encoding='utf-8')
    new_urls=self._get_new_urls(page_url,soup)
    data=self._get_new_data(page_url,soup)
    return new_urls,data

