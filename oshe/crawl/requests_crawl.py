import requests

from . import Crawl


class RequestsCrawl(Crawl):
    def __init__(self, headers=None, cookies=None, auth=None):
        super(RequestsCrawl, self).__init__(headers, cookies, auth)

    def get(self, url, **kwargs):
        try:
            headers = kwargs.pop('headers')
        except KeyError:
            headers = self.headers

        try:
            cookies = kwargs.pop('cookies')
        except KeyError:
            cookies = self.cookies

        raw = requests.get(url, headers=headers, cookies=cookies, **kwargs).text
        return raw
