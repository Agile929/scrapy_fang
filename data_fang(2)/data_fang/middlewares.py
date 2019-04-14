# -*- coding: utf-8 -*-
#
# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
# # -*- coding: utf-8 -*-
# class ProxyMiddleware(object):
#     def process_request(self, request, spider):
#         request.meta['proxy'] = "http://112.98.126.100:41578"
#

class DataFangSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# import time
# from selenium import webdriver
# from retrying import retry
#
# import scrapy
#
# class SeleniumMiddleware(object):
#     def __init__(self):
#         self.driver = webdriver.Chrome()
#
#     # 总共重试40次，每次间隔100毫秒
#     @retry(stop_max_attempt_number=40, wait_fixed=100)
#     def retry_load_page(self, request, spider):
#         # 如果页面数据找到了，表示网页渲染成功，程序正常向下执行
#         # 如果页面数据没找到，则抛出异常交给retry捕获，retry就会按照设置进行重试
#         #   - 如果在重试40次范围内找到了数据，程序正常执行
#         #   - 如果在重试40次范围后依然没有找到数据，表示该页面不能正常渲染，retry不再处理异常，则异常交给上一级调用的地方
#         try:
#             self.driver.find_element_by_xpath("//tbody/tr[2]/td[1]")
#         except:
#             self.count += 1
#             spider.logger.info("<{}> retry {} times".format(request.url, self.count))
#             # 手动抛出异常交给retry捕获，这样retry才能正常工作
#             raise Exception("<{}> page load failed.".format(request.url))
#
#
#     def process_request(self, request, spider):
#         # 判断url地址是否是动态页面的url，如果是的话则同chrome渲染处理；如果不是则通过下载器处理
#         if "monthdata" in request.url or "daydata" in request.url:
#
#             self.count = 0
#
#             self.driver.get(request.url)
#             # 显示等待
#             #time.sleep(2)
#
#             try:
#                 self.retry_load_page(request, spider)
#
#                 # 隐式等待
#                 #判断页面数据是否渲染成功，如果没成功继续等待，如果成功提取数据不用等待。
#
#                 # Unicode 字符串
#                 html = self.driver.page_source
#
#                 # 返回一个response响应对象给引擎，引擎会认为是下载器返回的响应，默认交给spider解析
#                 return scrapy.http.HtmlResponse(url=self.driver.current_url, body=html.encode("utf-8"), encoding="utf-8", request=request)
#
#             except Exception as e:
#                 spider.logger.error(e)
#                 return request



