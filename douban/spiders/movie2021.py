import scrapy
import re

from scrapy import Selector, Request

from ..items import Movie2021Item


class Movie2021Spider(scrapy.Spider):
    name = 'movie2021'
    allowed_domains = ['movie.douban.com']

    def start_requests(self):
        for page in range(25):
            page = page * 20
            url = 'https://m.douban.com/rexxar/api/v2/movie/recommend?refresh=0&start=%d&count=20&selected_categories={}&uncollect=false&tags=2021' % page
            yield Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        items: list = response.json().get('items')
        for item in items:
            movie2021_item = Movie2021Item()
            movie_id = int(item.get('id'))
            movie2021_item['movie_id'] = movie_id
            yield Request(
                url=f'https://movie.douban.com/subject/{movie_id}',
                callback=self.parse_movie,
                cb_kwargs={'item': movie2021_item}
            )

    def parse_movie(self, response, **kwargs):
        movie2021_item = kwargs['item']
        sel = Selector(response)
        # 标题
        movie2021_item['title'] = sel.css('span[property="v:itemreviewed"]::text').get().strip()
        # 类型
        types = sel.css('span[property="v:genre"]::text').getall()  # ['剧情', '喜剧', '奇幻']
        match (len(types)):
            case 0:
                movie2021_item['type1'] = ''
                movie2021_item['type2'] = ''
                movie2021_item['type3'] = ''
            case 1:
                movie2021_item['type1'] = types[0]
                movie2021_item['type2'] = ''
                movie2021_item['type3'] = ''
            case 2:
                movie2021_item['type1'] = types[0]
                movie2021_item['type2'] = types[1]
                movie2021_item['type3'] = ''
            case _:
                movie2021_item['type1'] = types[0]
                movie2021_item['type2'] = types[1]
                movie2021_item['type3'] = types[2]
        # 制片国家/地区
        movie2021_item['production_country'] = sel.xpath(
            '//*[@id="info"]/span[contains(text(),"制片国家/地区")]/following::text()[1]').get().strip()
        # 语言
        movie2021_item['language'] = sel.xpath(
            '//*[@id="info"]/span[contains(text(),"语言")]/following::text()[1]').get().strip()
        # 上映时间
        movie2021_item['release_date'] = sel.css('span[property="v:initialReleaseDate"]::text').get().strip()[:10]
        # 片长
        duration = sel.css('span[property="v:runtime"]::text').get()
        movie2021_item['duration'] = int(re.findall('\d+', duration)[0])
        # 评分
        movie2021_item['rank'] = float(sel.css('strong[property="v:average"]::text').get().strip())
        yield movie2021_item
