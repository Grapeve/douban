# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals, Request

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


# def get_cookies_dict():
#     cookies_str = 'gr_user_id=fe92a497-2c2c-4a53-a4b4-db66568d0d8b; ll="118282"; viewed="1465939_3012360_32581281_35539710"; bid=zyoUFEiNq0E; __gads=ID=fcbf8690268e1745-2255d06c40d800c0:T=1668173079:RT=1668173079:S=ALNI_MZUq7zZ4kabM6-XI7u3JHpROiZfpw; __utmz=30149280.1668690968.10.8.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __gpi=UID=000009b3c38d2997:T=1657168676:RT=1668690970:S=ALNI_MaR0eNPgFI7R_P_mZCp1Ll6EZNdsQ; _ga=GA1.2.1742431008.1631968181; push_noty_num=0; push_doumail_num=0; Hm_lvt_6d4a8cfea88fa457c3127e14fb5fabc2=1669898998,1669990271; _gid=GA1.2.1120349523.1669990271; ap_v=0,6.0; __utma=30149280.1742431008.1631968181.1670002441.1670031651.18; __utmb=30149280.0.10.1670031651; __utmc=30149280'
#     cookies_dict = {}
#     for item in cookies_str.split("; "):
#         if item != '':
#             key, value = item.split('=', maxsplit=1)
#             cookies_dict[key] = value
#     return cookies_dict
#
#
# COOKIES_DICT = get_cookies_dict()


class DoubanSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class DoubanDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request: Request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        request.headers['Accept'] = 'application/json, text/plain, */*'
        # request.headers['Accept-Encoding'] = 'gzip, deflate, br'
        request.headers['Referer'] = 'https://movie.douban.com/explore'
        request.headers[
            'Cookie'] = 'll="118297"; bid=U2Z1hOmx1Go; ap_v=0,6.0; __utma=30149280.286241461.1670742327.1670742327.1670742327.1; __utmb=30149280.0.10.1670742327; __utmc=30149280; __utmz=30149280.1670742327.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __gads=ID=ee94523dfe583e95-22c020acd0d800ba:T=1670742329:RT=1670742329:S=ALNI_MZAIwu_ZsjehX5s7e5ybREPmwLRkQ; __gpi=UID=00000b8e189262a5:T=1670742329:RT=1670742329:S=ALNI_MYfNitMNK6f_RQvlUIBPg8I7aHT-A'
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
