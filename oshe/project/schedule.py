class Schedule:
    def __init__(self, init_args=None, init_kwargs=None):
        self.tasks = []
        self.init_args = init_args or tuple()
        self.init_kwargs = init_kwargs or dict()

    def start(self):
        args = self.init_args
        kwargs = self.init_kwargs
        while self.tasks:
            task = self.tasks.pop(0)
            task = task(*args, **kwargs)
            args, kwargs = task.start()

    def add_task(self, task):
        self.tasks.append(task)
