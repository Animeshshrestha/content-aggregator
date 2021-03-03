from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from news_scrapping.spiders.ekantipur import EkantipurSpider
from news_scrapping.spiders.onlinekhabar import OnlinekhabarSpider
from news_scrapping.spiders.setopati import SetopatiSpider

if __name__ == '__main__':

    process = CrawlerProcess(get_project_settings())
    process.crawl(EkantipurSpider)
    process.crawl(OnlinekhabarSpider)
    process.crawl(SetopatiSpider)
    process.start()
