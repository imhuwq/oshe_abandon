from oshe.crawl.requests_crawl import RequestsCrawl


class SteamCraw(RequestsCrawl):
    def __init__(self):
        super(SteamCraw, self).__init__()

        self.headers = {
            'user-agent': 'User-Agent:Mozilla/5.0 (X11; Linux x86_64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/55.0.2883.75 Safari/537.36',
            'host': 'store.steampowered.com',
            'connection': 'keep-alive'
        }

        self.cookies = {'birthtime': '667753201',
                        'lastagecheckage': '1-March-1991',
                        'Steam_Language': 'english',
                        'steamCountry': 'CN',
                        'mature_content': '1'
                        }

    def get(self, url, **kwargs):
        headers = kwargs.pop('headers', None) or self.headers

        cookies = kwargs.pop('cookies', None) or self.cookies

        raw = self.requests.get(url, headers=headers, cookies=cookies, timeout=(5, 21), **kwargs).text
        return raw
