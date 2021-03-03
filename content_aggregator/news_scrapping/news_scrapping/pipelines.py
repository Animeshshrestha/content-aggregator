from itemadapter import ItemAdapter

from news.models import News


class NewsScrappingPipeline:
    def process_item(self, item, spider):
        if not News.objects.filter(link=item['link']).exists():
            news = News(**item)
            news.save()
        return item

