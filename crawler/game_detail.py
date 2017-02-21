from lxml import etree

from crawler.crawler_base import Crawler


class GameDetailCrawler(Crawler):
    def __init__(self, targets, *args, **kwargs):
        super(GameDetailCrawler, self).__init__(targets, *args, **kwargs)

    def parse_title(self, ehtml):
        details_container = ehtml.xpath('//div[@class="block_content_inner"]')[-1]
        detail_block = details_container.xpath('child::div[1]')[-1]
        texts = detail_block.xpath('text()')
        texts = self.clean_strings(texts)
        return texts[0]

    def parse_price(self, ehtml):
        price_unit = {
            '¥': 'CN',
            '$': 'US',
            'HK$': 'HK'
        }

        prices = {}
        try:
            price = ehtml.xpath('//div[@class="game_purchase_price price"]/text()')[0]
            if price:
                price = c.strip_strings([price])[0]
                unit, number = price.split(' ')

                current_number = origin_number = number
                country = price_unit.get(unit)
            else:
                current_number = origin_number = 0
                country = 'CN'

        except IndexError:
            origin_price = ehtml.xpath('//div[@class="discount_original_price"]/text()')[0]
            discount_price = ehtml.xpath('//div[@class="discount_final_price"]/text()')[0]

            origin_unit, origin_number = c.strip_strings([origin_price])[0].split(' ')
            current_unit, current_number = c.strip_strings([discount_price])[0].split(' ')
            country = price_unit.get(origin_unit)

        prices[country] = {'current': current_number, 'origin': origin_number}
        return prices

    def parse_tags(self, ehtml):
        tags = ehtml.xpath('//div[@class="glance_tags popular_tags"]')[-1]
        tags = tags.xpath('child::a/text()')
        tags = self.clean_strings(tags)
        return tags

    def parse_categories(self, ehtml):
        category_block = ehtml.xpath('//div[@id="category_block"]')[-1]
        category_list = category_block.xpath('descendant::a/text()')
        category_list = self.clean_strings(category_list)
        return category_list

    def parse_release_date(self, ehtml):
        details_container = ehtml.xpath('//div[@class="block_content_inner"]')[-1]
        detail_block = details_container.xpath('child::div[1]')[-1]
        texts = detail_block.xpath('text()')
        texts = self.clean_strings(texts)

        date_string = texts[-1]

        return date_string

    def parse_genre(self, ehtml):
        result = []

        details_container = ehtml.xpath('//div[@class="block_content_inner"]')[-1]
        detail_block = details_container.xpath('child::div[1]')[-1]
        detail_links = detail_block.xpath('a')

        detail_links_text = [link.xpath('text()')[0] for link in detail_links]

        detail_links_url = [link.xpath('@href')[-1] for link in detail_links]

        assert len(detail_links_text) == len(detail_links_url)

        for index in range(len(detail_links_text)):
            url = detail_links_url[index]
            if 'genre' in url:
                result.append(detail_links_text[index])

        return result

    def parse_developer(self, ehtml):
        result = []

        details_container = ehtml.xpath('//div[@class="block_content_inner"]')[-1]
        detail_block = details_container.xpath('child::div[1]')[-1]
        detail_links = detail_block.xpath('a')

        detail_links_text = [link.xpath('text()')[0] for link in detail_links]

        detail_links_url = [link.xpath('@href')[-1] for link in detail_links]

        assert len(detail_links_text) == len(detail_links_url)

        for index in range(len(detail_links_text)):
            url = detail_links_url[index]
            if 'developer' in url:
                result.append(detail_links_text[index])

        return result

    def parse_publisher(self, ehtml):
        result = []

        details_container = ehtml.xpath('//div[@class="block_content_inner"]')[-1]
        detail_block = details_container.xpath('child::div[1]')[-1]
        detail_links = detail_block.xpath('a')

        detail_links_text = [link.xpath('text()')[0] for link in detail_links]

        detail_links_url = [link.xpath('@href')[-1] for link in detail_links]

        assert len(detail_links_text) == len(detail_links_url)

        for index in range(len(detail_links_text)):
            url = detail_links_url[index]
            if 'publisher' in url:
                result.append(detail_links_text[index])

        return result

    def parse_languages(self, ehtml):
        result = {}

        language_options = ehtml.xpath('//table[@class="game_language_options"]')[-1]

        option_types = language_options.xpath('tr[1]/th/text()')

        language_rows = language_options.xpath('tr')[1:]

        for row in language_rows:
            tds = row.xpath('td')

            language = self.clean_strings([tds.pop(0).text])[0]

            language_option = {}

            for index, td in enumerate(tds):
                child = td.xpath('child::img')
                option_type = option_types[index]
                if child:
                    language_option[option_type] = True
                else:
                    language_option[option_type] = False

            result[language] = language_option

        return result

    def parse_requirements(self, ehtml):
        result = {}
        sys_req_block = ehtml.xpath('//div[@class="sysreq_contents"]')[-1]

        os_req_blocks = sys_req_block.xpath('child::div')

        for os_block in os_req_blocks:
            os_platform = os_block.xpath('@data-os')[-1]

            req_suits = os_block.xpath('*/ul')

            os_reqs = {}
            for suit in req_suits:
                suit_name = suit.xpath('strong/text()')
                suit_name = self.clean_strings(suit_name)[0].strip(':')

                os_reqs_list = {}
                req_list = suit.xpath('ul/li')
                for req_item in req_list:
                    req_string = req_item.xpath('string()').split(':', 1)
                    req_string = self.clean_strings(req_string)
                    os_reqs_list[req_string[0]] = req_string[1]

                os_reqs[suit_name] = os_reqs_list

            result[os_platform] = os_reqs

        return result

    def parse_all(self, html):
        title = self.parse_title(html)
        price = self.parse_price(html)
        tags = self.parse_tags(html)
        categories = self.parse_categories(html)
        release_date = self.parse_release_date(html)
        genre = self.parse_genre(html)
        developer = self.parse_developer(html)
        publisher = self.parse_publisher(html)
        languages = self.parse_languages(html)
        requirements = self.parse_requirements(html)

        data = {
            'title': title,
            'price': price,
            'tags': tags,
            'categories': categories,
            'release_date': release_date,
            'genre': genre,
            'developer': developer,
            'publisher': publisher,
            'languages': languages,
            'requirements': requirements
        }

        return data

    def parse(self, data):
        html = etree.HTML(data)
        data = self.parse_all(html)
        return data
