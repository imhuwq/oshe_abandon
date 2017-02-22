import os
import re
import time
import traceback
from enum import Enum
from concurrent import futures
from datetime import datetime

from oshe.store.sa_store import SqlalchemyStore
from oshe.crawl.requests_crawl import RequestsCrawl
from oshe.parse.xpath_parse import XpathParse


class Task:
    def __init__(self, targets, workers=16, crawler_cls=None, parse_cls=None, storer_cls=None, db_uri=None,
                 log_dir=None):
        self.targets = set(targets) if targets else set()

        self.results = list()

        self.searching = self.targets.copy()

        self.succeed = set()
        self.failed = set()

        self.fail_actions = []
        self.success_actions = []

        self.workers = workers

        self.timestamp = int(time.time())
        self.err_log = '%s.log' % self.timestamp

        self.log_dir = log_dir or os.path.abspath(os.path.dirname(__file__))
        self.err_log = os.path.join(self.log_dir, '%s_err.log' % self.timestamp)
        self.std_log = os.path.join(self.log_dir, '%s_std.log' % self.timestamp)

        self.parse_cls = parse_cls or XpathParse

        self.storer_cls = storer_cls or SqlalchemyStore
        self.db_uri = db_uri

        self.crawler_cls = crawler_cls or RequestsCrawl

        self.kwargs = {'workers': self.workers, 'crawler_cls': self.crawler_cls,
                       'parse_cls': self.parse_cls, 'storer_cls': self.storer_cls,
                       'db_uri': db_uri, 'log_dir': self.log_dir}

    def crawl(self, target):
        cookies = {
            'birthtime': '667753201',
            'lastagecheckage': '1-March-1991',
            'Steam_Language': 'english',
            'steamCountry': 'CN',
            'mature_content': '1'
        }

        crawler = self.crawler_cls(cookies=cookies)
        raw = crawler.get(target)
        return raw

    def parse(self, raw):
        data = self.parse_cls().parse(raw)
        self.results.extend(data)
        return data

    def store(self, data, target):
        store = self.storer_cls(self.db_uri)
        store.store(self.__class__.__name__, target, data)

    def task_chain(self, target):
        raw = self.crawl(target)
        data = self.parse(raw)
        self.store(data, target)

    def start(self, max_retries=3):
        print('')
        print(self.__class__.__name__ + ' started!')
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
                    self.log_std('[BAD]: <%s> "%s" ' % (target, exc))
                else:
                    self.succeed.add(target)
                    self.log_std('[OK]: <%s>' % target)

        self.failed, self.searching = self.searching, set()
        return (self.results,), self.kwargs

    def log_err(self, target, exc):
        with open(self.err_log, 'a') as f:
            log_text = '%s\n%s\n%s\n' % (datetime.now(), target, exc)
            f.write(log_text)
            traceback.print_exc(file=f)
            f.write('\n\n')

    def log_std(self, msg):
        print(self.log_dir)
        with open(self.std_log, 'a') as f:
            f.write(msg)
            f.write('\n')
