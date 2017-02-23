from lxml import etree

from oshe.parse.xpath_parse import XpathParse


class GameListParse(XpathParse):
    def __init__(self):
        self.base = 'http://store.steampowered.com/app/'
        super(GameListParse, self).__init__()

    def parse(self, data):
        html = etree.HTML(data)
        container = html.xpath('//div[@id="search_result_container"]')[-1]
        container = container.xpath('div[last()-1]')[-1]
        game_ids = container.xpath('child::a//@data-ds-appid')

        results = []
        for game_id in game_ids:
            result = self.base + game_id
            results.append(result)
        return results, results
