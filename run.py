from crawler.game_index import GameIndexCrawler
from crawler.game_list import GameListCrawler
from crawler.game_detail import GameDetailCrawler

index_page = 'http://store.steampowered.com/search/?sort_by=Released_DESC'

index_crawler = GameIndexCrawler([index_page])
index_crawler.start()

print(len(index_crawler.results))
list_crawler = GameListCrawler(index_crawler.results)
list_crawler.start()

print(len((list_crawler.results)))

detail_crawler = GameDetailCrawler(list_crawler.results)
detail_crawler.start()
