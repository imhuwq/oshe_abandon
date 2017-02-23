from . import ParseBase


class XpathParse(ParseBase):
    def __init__(self):
        super(XpathParse, self).__init__()

    def parse(self, data):
        results = targets = data
        return results, targets
