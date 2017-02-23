import os

from .schedule import Schedule


class Project:
    def __init__(self, name, project_dir):
        self.name = name

        self.project_dir = project_dir
        self.data_dir = self.project_dir + '/data'
        os.makedirs(self.data_dir, exist_ok=True)

        self.log_dir = self.project_dir + '/logs'
        os.makedirs(self.log_dir, exist_ok=True)

        self.db_uri = 'sqlite:///%s/%s.sqlite' % (self.data_dir, self.name)

        self._schedule = Schedule()

    def start(self):
        self._schedule.start()

    def schedule(self, task, name=None, targets=None, workers=16,
                 crawl_cls=None, parse_cls=None, store_cls=None,
                 db_uri=None, log_dir=None):
        db_uri = db_uri or self.db_uri
        log_dir = log_dir or self.log_dir

        kwargs = dict(name=name,
                      workers=workers,
                      crawl_cls=crawl_cls,
                      parse_cls=parse_cls,
                      store_cls=store_cls,
                      db_uri=db_uri,
                      log_dir=log_dir)

        self._schedule.add_task(task, targets, kwargs)
