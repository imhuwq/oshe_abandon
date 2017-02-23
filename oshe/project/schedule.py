class Schedule:
    def __init__(self):
        self.tasks = []

    def start(self):
        next_targets = list()

        while self.tasks:
            task_cls, task_targets, task_kwargs = self.tasks.pop(0)
            task_targets = task_targets or next_targets
            task = task_cls(task_targets, **task_kwargs)
            next_targets = task.start()

    def add_task(self, task, targets, kwargs):
        self.tasks.append([task, targets, kwargs])
