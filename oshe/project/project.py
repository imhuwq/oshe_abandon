import os

from .schedule import Schedule


class Project:
    def __init__(self, name, project_dir, init_args=None, init_kwargs=None):
        self.name = name

        self.project_dir = project_dir
        self.data_dir = self.project_dir + '/data'
        os.makedirs(self.data_dir, exist_ok=True)

        self.log_dir = self.project_dir + '/logs'
        os.makedirs(self.log_dir, exist_ok=True)

        self.db_uri = 'sqlite:///%s/%s.sqlite' % (self.data_dir, self.name)
        init_args = init_args or tuple()
        init_kwargs = init_kwargs or dict()

        init_kwargs.update(db_uri=self.db_uri, log_dir=self.log_dir)
        self._schedule = Schedule(init_args=init_args, init_kwargs=init_kwargs)

    def start(self):
        self._schedule.start()

    def schedule(self, task):
        self._schedule.add_task(task)
