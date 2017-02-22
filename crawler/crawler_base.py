import re
import os
import time
import traceback
from datetime import datetime
from concurrent import futures

import requests

from storer.sa_store import SqlalchemyStore


class Crawler:
    def __init__(self, targets=None, workers=16, storer_cls=None):

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

        cur_dir = os.path.abspath(os.path.dirname(__file__))
        self.err_log = os.path.join(cur_dir, '%s_err.log' % self.timestamp)
        self.std_log = os.path.join(cur_dir, '%s_std.log' % self.timestamp)

        self.storer_cls = storer_cls or SqlalchemyStore

        self.round = 0

    def strip_strings(self, strings):
        result = []
        pattern = re.compile(r'^([\t\n\s]*)(?P<item>.*?)([\t\n\s]*)$')
        for item in strings:
            item = pattern.sub(r'\g<item>', item)
            result.append(item)
        return result

    def clean_strings(self, strings):
        strings = self.strip_strings(strings)

        def string_is_meaningful(string):
            if len(string) == 1:
                has_meaningful_char = re.match(r'[a-zA-Z0-9]', string)
                if has_meaningful_char:
                    return True
            elif len(string) > 1:
                return True
            return False

        result = [string for string in strings if string_is_meaningful(string)]
        return result

    def crawl(self, target):
        cookies = {
            'birthtime': '667753201',
            'lastagecheckage': '1-March-1991',
            'Steam_Language': 'english',
            'steamCountry': 'CN',
            'mature_content': '1'
        }

        raw = requests.get(target, cookies=cookies).text
        return raw

    def parse(self, raw):
        data = raw
        return data

    def store(self, data, target):
        store = self.storer_cls()
        store.store(self.__class__.__name__, target, data)

    def task_chain(self, target):
        raw = self.crawl(target)
        data = self.parse(raw)
        if data is None:
            data = self.results
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
