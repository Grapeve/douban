# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import openpyxl
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class DoubanPipeline:

    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.ws.title = "Movie2021"
        self.ws.append(
            ("电影ID", "标题", "类型1", "类型2", "类型3", "制片国家/地区", "语言", "上映日期", "片长", "评分"))

    def close_spider(self, spider):
        self.wb.save('电影数据2021.xlsx')

    def process_item(self, item, spider):
        movie_id = item.get('movie_id', '')
        title = item.get('title', '')
        type1 = item.get('type1', '')
        type2 = item.get('type2', '')
        type3 = item.get('type3', '')
        production_country = item.get('production_country', '')
        language = item.get('language', '')
        release_date = item.get('release_date', '')
        duration = item.get('duration', '')
        rank = item.get('rank', '')
        self.ws.append(
            (movie_id, title, type1, type2, type3, production_country, language, release_date, duration, rank,))
        return item
