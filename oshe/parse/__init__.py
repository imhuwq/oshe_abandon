class ParseBase:
    def __init__(self):
        pass

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

    def parse(self, data):
        return data
