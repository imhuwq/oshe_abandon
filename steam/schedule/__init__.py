from celery import Celery
from steam.tasks.game_detail import GameDetailCrawl, GameDetailParse, GameDetailStore
from steam.tasks.game_index import GameIndexCrawl, GameIndexParse

from steam.tasks.game_list import GameListCrawl, GameListParse

celery_app = Celery('tasks')
celery_app.conf.broker_url = 'redis://localhost:6379/0'
celery_app.conf.result_backend = 'redis://localhost:6379/0'


@celery_app.task
def crawl_index(target):
    crawler = GameIndexCrawl()
    raw = crawler.get(target)
    parse_index.delay(raw)


@celery_app.task
def parse_index(raw):
    parser = GameIndexParse()
    results = parser.parse(raw)
    for result in results:
        crawl_list.delay(result)


@celery_app.task
def crawl_list(target):
    crawler = GameListCrawl()
    raw = crawler.get(target)
    parse_list.delay(raw)


@celery_app.task
def parse_list(raw):
    parser = GameListParse()
    results = parser.parse(raw)
    for result in results:
        crawl_detail.delay(result)


@celery_app.task
def crawl_detail(target):
    crawler = GameDetailCrawl()
    raw = crawler.get(target)
    parse_detail.delay(raw)


@celery_app.task
def parse_detail(raw):
    parser = GameDetailParse()
    results = parser.parse(raw)
    for result in results:
        store_detail.delay(result)


@celery_app.task
def store_detail(data):
    store = GameDetailStore()
    collection = 'steam'
    identity = data.get('title')
    store.store(collection, identity, data)

# TODO: the celery app should be configurable
# TODO: there must be a better way to organize these celery task!
