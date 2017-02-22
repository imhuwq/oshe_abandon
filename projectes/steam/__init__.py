import os

from oshe.project import Project

from .tasks.game_index import GameIndexTask
from .tasks.game_list import GameListTask
from .tasks.game_detail import GameDetailTask

cur_dir = os.path.dirname(os.path.abspath(__file__))

index_page = 'http://store.steampowered.com/search/?sort_by=Released_DESC'

steam = Project('steam', cur_dir, init_args=([index_page],))

steam.schedule(GameIndexTask)
# steam.schedule(GameListTask)
# steam.schedule(GameDetailTask)
