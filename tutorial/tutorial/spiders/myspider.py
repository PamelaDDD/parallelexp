import re
import threading
from urllib import parse
import scrapy.exceptions

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['https://web.mit.edu/research/']
    cnt = 0
    lock = threading.Lock()
    url_regex = re.compile(r'^((https|http)?://)[^\s]+')


    def parse(self, response,**kwargs):
        QuotesSpider.lock.acquire()
        filename = '/Users/duwenjing/Downloads/parallelexpdata/%d.html' % QuotesSpider.cnt
        QuotesSpider.cnt += 1
        QuotesSpider.lock.release()
        with open(filename,'w') as f:
            f.write(str(response.body))
        try:
            for a in response.css('a'):
                try:
                    next_page = a.attrib['href']
                except KeyError:
                    print('no href in a, a={}'.format(a))
                    continue

                next_page = parse.urljoin(response.url,next_page)
                if not QuotesSpider.url_regex.match(next_page):
                    print('invalid http(s) URL,next_page={}'.format(next_page))
                    continue
                print('next_page:',next_page)

                yield response.follow(next_page,self.parse)
        except scrapy.exceptions.NotSupported as e:
            print('invalid response, e={}'.format(e))


