from lxml import etree

from crawler.crawler_base import Crawler


class GameIndexCrawler(Crawler):
    def __init__(self, targets, *args, **kwargs):
        self.base = 'http://store.steampowered.com/search/?sort_by=Released_DESC'
        super(GameIndexCrawler, self).__init__(targets, *args, **kwargs)

    def store(self, data, target):
        pass

    def parse(self, data):
        html = etree.HTML(data)
        pagination = html.xpath('//div[@class="search_pagination_right"]')[-1]
        last_page = pagination.xpath('a[last()-1]')[0]
        last_page = int(last_page.text)

        for page in range(1, last_page + 1):
            result = '%s&page=%d' % (self.base, page)
            self.results.append(result)
