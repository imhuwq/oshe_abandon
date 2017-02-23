from lxml import etree

from oshe.parse.xpath_parse import XpathParse


class GameIndexParse(XpathParse):
    def __init__(self):
        super(GameIndexParse, self).__init__()
        self.base = 'http://store.steampowered.com/search/?sort_by=Released_DESC'

    def parse(self, data):
        results = []
        html = etree.HTML(data)
        pagination = html.xpath('//div[@class="search_pagination_right"]')[-1]
        last_page = pagination.xpath('a[last()-1]')[0]
        last_page = int(last_page.text)

        for page in range(1, last_page + 1):
            result = '%s&page=%d' % (self.base, page)
            results.append(result)
        return results, results
