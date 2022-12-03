# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# 爬虫获取到的数据需要组装成Item对象
class MovieItem(scrapy.Item):
    title = scrapy.Field()
    rank = scrapy.Field()
    subject = scrapy.Field()
    duration = scrapy.Field()
    intro = scrapy.Field()


class Movie2021Item(scrapy.Item):
    movie_id = scrapy.Field()
    title = scrapy.Field()
    type1 = scrapy.Field()
    type2 = scrapy.Field()
    type3 = scrapy.Field()
    production_country = scrapy.Field()
    language = scrapy.Field()
    release_date = scrapy.Field()
    duration = scrapy.Field()
    rank = scrapy.Field()
    rating_people = scrapy.Field()
