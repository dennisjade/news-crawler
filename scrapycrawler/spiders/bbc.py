import scrapy
from scrapycrawler.items import NewsItem


# parse "bbc.com" news posted in the homepage thumbnails
class BbcSpider(scrapy.Spider):
    name = 'bbc'
    allowed_domains = ["bbc.com"]
    start_urls = ['http://www.bbc.com/']

    def parse(self, response):
        # follow links to news page
        for href in response.css('.media__link::attr(href)'):
            
            if href is not None:
                yield response.follow(href, callback=self.parse_newspage)

    def parse_newspage(self, response):
        # find the element in the DOM
        # query = array of possible dOM structure to find
        def clean_data(query):
            data = []
            for q in query:
                data = response.css(q).extract_first()

                if data:
                    # if data is found, do not iterate thru other fields
                    break

            return data

        item = NewsItem()
        item['title'] = clean_data([
            'h1.story-body__h1::text',
            'h1.gallery-intro__h1::text',
            'h1.vxp-media__headline::text'
            ])
        item['summary'] = clean_data([
            'p.story-body__introduction::text',
            'p.gallery-intro__summary::text',
            'div.vxp-media__summary p::text'
            ])
        item['body'] = clean_data([
            'div.story-body__inner p::text',
            'p.gallery-images__summary::text'])
        item['url'] = response.url

        yield item