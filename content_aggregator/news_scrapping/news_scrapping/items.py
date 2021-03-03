import scrapy

class NewsScrappingItem(scrapy.Item):

    category = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    description = scrapy.Field()
    images_link = scrapy.Field()


