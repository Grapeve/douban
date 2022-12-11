# Scripy爬取豆瓣2021年所有电影

目录下的requirements.txt存放了该项目所需要的库的版本。

可以在一个新建的虚拟环境下（由于我所用的虚拟环境安装了很多乱七八糟的第三方库，结果一并写入了requirements.txt，实际真实需要的并没有这么多第三方库）

```python
pip install -r requirements.txt
```



## 1. 项目运行

1. 前往middlewares.py中配置自己的Cookie。

![](C:\Users\DELL\AppData\Roaming\marktext\images\2022-12-11-15-08-10-image.png)

获取Cookie，前往 https://movie.douban.com/explore ，打开F12，选择网络一栏。点击页面**年代**选**2021**，

![](https://s1.ax1x.com/2022/12/11/zhCmr9.png)

![](https://s1.ax1x.com/2022/12/11/zhC6MQ.png)

2.前往终端运行

```python
scrapy crawl movie2021 -o movie2021.csv
```

爬取完后会生成**movie2021.csv**和**电影数据2021.xlsx**两种格式文件，xlsx格式配置在pipelines.py实现。

## 2. 项目流程

为爬取豆瓣2021年所有上映电影信息，需先获取上映电影的所有**id**，再通过 https://movie.douban.com/subject/{ id }去该电影详情页面获取该电影详细信息。

### 1.获取2021年所有上映电影id

通过对网页请求的观察，发现了豆瓣电影数据的一个请求api：

`https://m.douban.com/rexxar/api/v2/movie/recommend?refresh=0&start=100&count=20&selected_categories=%7B%7D&uncollect=false&tags=2021`

其中`start`参数表示所请求电影数据所在位置，`count`表示请求电影数目。`tags`表示查询电影的年份。

同时，在观察时发现`start`的值最小为0，最大为480，故可请求25次，在其response中收集所有电影id。若明确2021年豆瓣所收纳的电影数目，可将`count`的数值直接改为具体的数目。这样有助于减少被豆瓣发现异常的几率。

**部分代码：**

**spiders \ movie2021.py**

```python
class Movie2021Spider(scrapy.Spider):
    name = 'movie2021'
    allowed_domains = ['movie.douban.com']

    def start_requests(self):
        for page in range(25):
            page = page * 20
            url = 'https://m.douban.com/rexxar/api/v2/movie/recommend?refresh=0&start=%d&count=20&selected_categories={}&uncollect=false&tags=2021&ck=9-oe' % page
            yield Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        items: list = response.json().get('items')
        for item in items:
            # Movie2021Item是在items.py中定义, 
            # 用于将爬取到的数据组装成一个对象
            movie2021_item = Movie2021Item()
            movie_id = int(item.get('id'))  # 获取电影id
            movie2021_item['movie_id'] = movie_id
            yield Request(    # 跳转电影详情页
                url=f'https://movie.douban.com/subject/{movie_id}',
                callback=self.parse_movie,  # 电影详情页解析函数
                cb_kwargs={'item': movie2021_item}  
            )
```

**items.py**  (将爬取到数据封装成一个item对象)

```python
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
```

### 2.获取电影详细信息

在进入电影详情页面后，观察需要爬取的信息级网页结构

![](https://s1.ax1x.com/2022/12/11/zhFLZj.png)

可利用**css选择器**或**xpath**进行获取所需要的信息：

**movie2021.py**

```python
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
            '//*[@id="info"]/span[contains(text(),"语言")]/following::text()[1]').get()
        # 上映时间
        movie2021_item['release_date'] = sel.css('span[property="v:initialReleaseDate"]::text').get().strip()[:10]
        # 片长
        duration = sel.css('span[property="v:runtime"]::text').get()
        movie2021_item['duration'] = int(re.findall('\d+', duration)[0])
        # 评分
        movie2021_item['rank'] = float(sel.css('strong[property="v:average"]::text').get().strip())
        # 评价人数
        movie2021_item['rating_people'] = int(sel.css('span[property="v:votes"]::text').get())

        yield movie2021_item
```

### 3.输出xlsx格式配置

由于scrapy不能直接输出xlsx格式，需手动在pipelines中进行配置。

这里使用了**openpyxl**这个第三方库

**pipelines.py**

```python
class DoubanPipeline:

    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.ws.title = "Movie2021"
        self.ws.append(
            ("电影ID", "电影名", "类型1", "类型2", "类型3", "制片国家/地区", "语言", "上映日期", "片长", "评分",
             "评价人数"))

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
        rating_people = item.get('rating_people', '')
        self.ws.append(
            (movie_id, title, type1, type2, type3, production_country, language, release_date, duration, rank,
             rating_people))
        return item

```


