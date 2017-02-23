import os
import time
import traceback
from concurrent import futures
from datetime import datetime

from oshe.store.sa_store import SqlalchemyStore
from oshe.crawl.requests_crawl import RequestsCrawl


class Task:
    def __init__(self, targets, name=None, workers=16, crawl_cls=None, parse_cls=None, store_cls=None, db_uri=None,
                 log_dir=None):
        self.targets = list(targets) if targets else list()

        self.name = name or self.__class__.__name__

        self.results = list()
        self.next_targets = list()

        self.searching = self.targets.copy()

        self.succeed = set()
        self.failed = set()

        self.fail_actions = []
        self.success_actions = []

        self.workers = workers

        self.timestamp = int(time.time())
        self.err_log = '%s.log' % self.timestamp

        self.log_dir = log_dir or os.path.abspath(os.path.dirname(__file__))
        self.err_log = os.path.join(self.log_dir, '%s_%s_err.log' % (self.name, self.timestamp))
        self.std_log = os.path.join(self.log_dir, '%s_%s_std.log' % (self.name, self.timestamp))

        self.parse_cls = parse_cls

        self.store_cls = store_cls or SqlalchemyStore
        self.db_uri = db_uri

        self.crawl_cls = crawl_cls or RequestsCrawl

        self.kwargs = {'workers': self.workers, 'crawl_cls': self.crawl_cls,
                       'parse_cls': self.parse_cls, 'store_cls': self.store_cls,
                       'db_uri': self.db_uri, 'log_dir': self.log_dir}

    def crawl(self, target):
        crawler = self.crawl_cls()
        raw = crawler.get(target)
        return raw

    def parse(self, raw):
        current_results, next_targets = self.parse_cls().parse(raw)
        return current_results, next_targets

    def store(self, data, target):
        store = self.store_cls(self.db_uri)
        store.store(self.name, target, data)

    def task_chain(self, target):
        raw = self.crawl(target)

        current_result, next_targets = self.parse(raw)

        self.next_targets.extend(next_targets)
        self.store(current_result, target)

    def start(self):
        print('')
        print('%s started! <%s> to go!' % (self.name, len(self.targets)))
        print('')
        with futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
            future_to_target = {executor.submit(self.task_chain, target): target
                                for target in self.searching}
            self.searching = set()
            for future in futures.as_completed(future_to_target):
                target = future_to_target[future]
                try:
                    future.result()
                except Exception as exc:
                    self.log_err(target, exc)
                    self.searching.add(target)
                    msg = '[BAD]: <%s> "%s" ' % (target, exc)
                    self.log_err(target, msg)
                else:
                    self.succeed.add(target)
                    msg = '[OK]: <%s>' % target
                    self.log_std(msg)

        return self.next_targets

    def log_err(self, target, exc):
        with open(self.err_log, 'a') as f:
            log_text = '%s\n%s\n%s\n' % (datetime.now(), target, exc)
            f.write(log_text)
            traceback.print_exc(file=f)
            f.write('\n\n')

    def log_std(self, msg):
        with open(self.std_log, 'a') as f:
            f.write(msg)
            f.write('\n')
