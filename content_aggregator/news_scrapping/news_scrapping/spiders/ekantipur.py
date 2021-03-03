from scrapy import Spider
import unicodedata

from scrapy.http import Request

from news_scrapping.items import NewsScrappingItem



class EkantipurSpider(Spider):
    name = 'ekantipur'
    allowed_domains = ['ekantipur.com']
    start_urls = ['http://ekantipur.com']

    def parse(self, response):

        navigation_extracted_links = response.xpath('//*[@id="header"]/div[1]/nav/div/div[2]/div/ul/li/a/@href').getall()
        navigation_links = list(filter(lambda link: 'https://ekantipur.com/' in link, navigation_extracted_links))
        for link in navigation_links:
            yield Request(link, callback=self.parse_link, dont_filter=True)
    
    def parse_link(self,response):

        item = NewsScrappingItem()
        news_category = response.url.split('https://ekantipur.com/')[1]
        base_link = response.xpath('//div[contains(@class, "col-xs-10 col-sm-10 col-md-10")]//article')
        for response in base_link:
            category = "OTHERS" if news_category == "Other" else news_category.upper()
            title = response.xpath('div[contains(@class,"teaser offset")]/h2/a/text()').get()
            link = self.start_urls[0]+response.xpath('div[contains(@class,"teaser offset")]/h2/a/@href').get()
            description = response.xpath('div[contains(@class,"teaser offset")]/p/text()').get()
            images_link = response.xpath('div[contains(@class,"image")]/figure/a/img/@data-src').get()

            item['category'] = category
            item['title'] = unicodedata.normalize("NFKD",title)
            item['link'] = link
            item['description'] = unicodedata.normalize("NFKD",description)
            item['images_link'] = images_link

            yield item
        
