import os

from oshe.project import Project

from oshe.task import Task

from .tasks import SteamCraw
from .tasks.game_index import GameIndexParse
from .tasks.game_list import GameListParse
from .tasks.game_detail import GameDetailParse

cur_dir = os.path.dirname(os.path.abspath(__file__))

index_page = 'http://store.steampowered.com/search/?sort_by=Released_DESC'

steam = Project('steam', cur_dir)

steam.schedule(Task,
               targets=[index_page],
               name='IndexCrawl',
               crawl_cls=SteamCraw,
               parse_cls=GameIndexParse)

steam.schedule(Task,
               name='ListCrawl',
               crawl_cls=SteamCraw,
               parse_cls=GameListParse)

steam.schedule(Task,
               name='DetailCrawl',
               crawl_cls=SteamCraw,
               parse_cls=GameDetailParse)
