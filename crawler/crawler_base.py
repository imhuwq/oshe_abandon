import re
import os
import time
import traceback
from datetime import datetime
from concurrent import futures

import requests


class Crawler:
    def __init__(self, targets=None, workers=4):

        self.targets = set(targets) if targets else set()

        self.results = list()

        self.searching = self.targets.copy()

        self.succeed = set()
        self.failed = set()

        self.fail_actions = []
        self.success_actions = []

        self.workers = workers

        self.timestamp = int(time.time())
        self.log_file = '%s.log' % self.timestamp

        cur_dir = os.path.abspath(os.path.dirname(__file__))
        role_dir = os.path.join(cur_dir, 'result', self.__class__.__name__)

        self.log_file = os.path.join(cur_dir, '%s.log' % self.timestamp)
        self.out_dir = role_dir
        os.makedirs(self.out_dir, exist_ok=True)

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
            'steamCountry': 'CN'
        }

        raw = requests.get(target, cookies=cookies).text
        return raw

    def parse(self, raw):
        data = raw
        return data

    def store(self, data, target):
        raise NotImplementedError

    def task_chain(self, target):
        raw = self.crawl(target)
        data = self.parse(raw)
        self.store(data, target)

    def start(self, max_retries=3):
        while self.searching and max_retries > 0:
            with futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
                future_to_target = {executor.submit(self.task_chain, target): target
                                    for target in self.searching}
                self.searching = set()
                for future in futures.as_completed(future_to_target):
                    target = future_to_target[future]
                    try:
                        future.result()
                    except Exception as exc:
                        self.log(target, exc)
                        self.searching.add(target)
                        print('[BAD]: <%s> "%s" ' % (target, exc))
                    else:
                        self.succeed.add(target)
                        print('[OK]: <%s>' % target)

            max_retries -= 1

        self.failed, self.searching = self.searching, set()

    def log(self, target, exc):
        with open(self.log_file, 'a') as f:
            log_text = '%s\n%s\n%s\n' % (datetime.now(), target, exc)
            f.write(log_text)
            traceback.print_exc(file=f)
            f.write('\n\n')
