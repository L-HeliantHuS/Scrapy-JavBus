# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

class RefererMiddleware(object):
    def process_request(self, request, spider):
        request.headers["Referer"] = "https://www.javbus.com"