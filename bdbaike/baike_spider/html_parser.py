from bs4 import BeautifulSoup
import re
import urlparse


class HtmlParser(object):

    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        links = soup.find_all('a', href=re.compile(r"/view/\d+\.htm"))
        for link in links:
            new_url = link['href']
            new_full_url = urlparse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self, page_url, soup):
        #  with open('souplog.log', 'w') as f:
            #  f.write('soup:\n%s' % ())
        res_data = {}

        title_node = soup.find('dd', class_="lemmaWgt-lemmaTitle-title").find("h1")
        #  print title_node
        res_data['title'] = title_node.get_text()

        summary_node = soup.find('div', class_="lemma-summary")
        #  print summary_node
        res_data['summary'] = summary_node.get_text()
        res_data['url'] = page_url
        #  for k in res_data:
            #  print res_data[k]
        return res_data

    def parse(self, page_url, html_cont):
        #  with open('testlog.log', 'w') as f:
            #  f.write('page_url: %s\n\nhtml:\n\n%s' % (page_url, html_cont))
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data
