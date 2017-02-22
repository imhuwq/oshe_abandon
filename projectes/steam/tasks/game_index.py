from lxml import etree

from oshe.task import Task
from oshe.parse.xpath_parse import XpathParse


class ParseGameIndex(XpathParse):
    def __init__(self):
        super(ParseGameIndex, self).__init__()
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
        return results


class GameIndexTask(Task):
    def __init__(self, targets, *args, parse_cls=ParseGameIndex, **kwargs):
        super(GameIndexTask, self).__init__(targets, *args, parse_cls=ParseGameIndex, **kwargs)
