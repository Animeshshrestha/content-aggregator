import scrapy
import unicodedata

from scrapy.http import Request

from news_scrapping.items import NewsScrappingItem


class SetopatiSpider(scrapy.Spider):
    name = 'setopati'
    allowed_domains = ['setopati.com']
    start_urls = ['http://setopati.com/']

    def parse(self, response):

        navigation_extracted_links = response.xpath('//*[@id="header"]/div[2]/div/div/div/ul/li[not(@class)]/a/@href').extract()
        for link in navigation_extracted_links:
            yield Request(link, callback=self.parse_link, dont_filter=True)
    
    def parse_link(self,response):

        item = NewsScrappingItem()
        news_category = response.url.split('https://www.setopati.com/')[1:]*3
        base_link = response.xpath('//*[@id="content"]/div/section/div[not(contains(@class,"alt")) and not(contains(@class,"pagination")) and not(contains(@class,"special-featured-box"))]')
        for response in base_link:
            title = response.xpath('div/a/@title').extract()
            link = response.xpath('div/a/@href').extract()
            images_link = response.xpath('div/a/figure/img/@src').extract()
            category = news_category
            list_of_news = [{'title': title, 'link': link, 'images_link': images_link,'category':category} \
                              for title, link , images_link, category \
                              in zip(title, link, images_link, category)
                            ]
            for news in list_of_news:
                item['category'] = news['category']
                item['title'] = unicodedata.normalize("NFKD",news['title'])
                item['link'] = news['link']
                item['description'] = None
                item['images_link'] = news['images_link']

                yield item
