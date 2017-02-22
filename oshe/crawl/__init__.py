class Crawl:
    def __init__(self, headers=None, cookies=None, auth=None):
        self.headers = headers
        self.cookies = cookies
        self.auth = auth

    def get(self, url, **kwargs):
        raise NotImplementedError

    def post(self, url, **kwargs):
        pass

    def option(self, url, **kwargs):
        pass

    def delete(self, url, **kwargs):
        pass

    def login(self, **kwargs):
        pass

    def logout(self):
        pass
