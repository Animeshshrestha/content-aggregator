import scrapy
import unicodedata

from scrapy.http import Request

from news_scrapping.items import NewsScrappingItem


class OnlinekhabarSpider(scrapy.Spider):
    name = 'onlinekhabar'
    allowed_domains = ['onlinekhabar.com']
    start_urls = ['http://onlinekhabar.com/']
    news_category_substitutions = {
        'prabhas-news':'OTHERS',
        'news':'NEWS',
        'business/technology':'TECHNOLOGY',
    }

    def parse(self, response):

        navigation_extracted_links = set(response.xpath('//*[@id="site-navigation"]/div/ul/li/a/@href').extract())
        filtered_links = [link for link in list(navigation_extracted_links) if "/content/" in link]
        for link in filtered_links:
            yield Request(link, callback=self.parse_link, dont_filter=True)
    
    def parse_link(self,response):

        item = NewsScrappingItem()
        news_category = response.url.split('https://www.onlinekhabar.com/content/')[1]
        news_category_replacement = self.news_category_substitutions[news_category]
        base_link = response.xpath('//*[@id="main"]/section/div/div/div/div[3]/div[contains(@class,"relative list__post show_grid--view")]')
        for response in base_link:
            category = news_category_replacement
            title = response.xpath('div[contains(@class,"item")]/div/a/text()').get()
            link = response.xpath('div[contains(@class,"item")]/div/a/@href').get()
            description = response.xpath('div[contains(@class,"item")]/div/p/text()').get()
            images_link = response.xpath('div[contains(@class,"item hasImg")]/a/img/@src').get()

            item['category'] = category
            item['title'] = unicodedata.normalize("NFKD",title)
            item['link'] = link
            item['description'] = unicodedata.normalize("NFKD",description)
            item['images_link'] = images_link

            yield item