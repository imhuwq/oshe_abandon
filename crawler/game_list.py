from lxml import etree

from crawler.crawler_base import Crawler


class GameListCrawler(Crawler):
    def __init__(self, targets, *args, **kwargs):
        self.base = 'http://store.steampowered.com/app/'
        super(GameListCrawler, self).__init__(targets, *args, **kwargs)

    def parse(self, data):
        html = etree.HTML(data)
        container = html.xpath('//div[@id="search_result_container"]')[-1]
        container = container.xpath('div[last()-1]')[-1]
        game_ids = container.xpath('child::a//@data-ds-appid')

        results = []
        for game_id in game_ids:
            result = self.base + game_id
            self.results.append(result)
            results.append(result)
        return results
