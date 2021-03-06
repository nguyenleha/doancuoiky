import scrapy


def parse_author(response):
    def extract_with_css(query):
        return response.css(query).get(default='').strip()
    print(extract_with_css("#storybox > h1"))
    yield {
        'name': extract_with_css("#storybox > h1::text"),
        'birthdate': extract_with_css('.author-born-date::text'),
        'bio': extract_with_css('.author-description::text'),
    }


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        url = 'https://thanhnien.vn/tai-chinh-kinh-doanh/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        author_page_links = response.xpath('/html/body/form/div[1]/div/div[2]/div[5]/div[1]/div[1]/div[1]/div/article[1]/h2/a')
        yield from response.follow_all(author_page_links, parse_author)

        pagination_links = response.css('li.next a')
        yield from response.follow_all(pagination_links, self.parse)

