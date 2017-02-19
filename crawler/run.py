from crawler.game_index import GameIndexCrawler
from crawler.game_list import GameListCrawler

index_page = 'http://store.steampowered.com/search/?sort_by=Released_DESC'

index_crawler = GameIndexCrawler([index_page])
index_crawler.start()

list_crawler = GameListCrawler(index_crawler.results)
list_crawler.start()


print(list_crawler.results)
