#!/usr/bin/env python
# coding=utf-8

import re
import os
import scrapy
import requests
import sys
import time
from os.path import abspath, join, dirname
upper_path = abspath(join(abspath(dirname(__file__)),'..'))
sys.path.append(upper_path)
reload(sys)
sys.setdefaultencoding('utf-8')

class MainSpider(scrapy.Spider):
    name = 'NewZl_spider'
    start_urls = (
        'http://legislation.govt.nz/subscribe/',
    )

    def parse(self, response):
        print('in parse --- ---')
        subscribe_page = response.xpath('//li[@class="directory"]/a/@href').extract()
        for per_url in subscribe_page:
            full_link = response.urljoin(per_url)
            print(full_link)
            yield scrapy.Request(full_link, callback=self.parse_secondPage)

    def parse_secondPage(self, response):
        print('in parse_secondPage --- ---')
        second_Page = response.xpath('//li[@class="directory"]/a/@href').extract()
        for per_url in second_Page:
            full_link = response.urljoin(per_url)
            print(full_link)
            yield scrapy.Request(full_link, callback=self.parse_thirtPage)

    def parse_thirtPage(self, response):
        print('in parse_thirtPage --- ---')
        third_Page = response.xpath('//li[@class="directory"]/a/@href').extract()
        for per_url in third_Page:
            full_link = response.urljoin(per_url)
            print(full_link)
            yield scrapy.Request(full_link, callback=self.parse_fourthPage)

    def parse_fourthPage(self, response):
        print('in parse_fourthPage --- ---')
        fourth_Page = response.xpath('//li[@class="directory"]/a/@href').extract()
        for per_url in fourth_Page:
            full_link = response.urljoin(per_url)
            print(full_link)
            yield scrapy.Request(full_link, callback=self.parse_fifthPage)

    def parse_fifthPage(self, response):
        print('in parse_fourthPage --- ---')
        fifth_Page = response.xpath('//li[@class="directory"]/a/@href').extract()
        for per_url in fifth_Page:
            full_link = response.urljoin(per_url)
            print(full_link)
            yield scrapy.Request(full_link, callback=self.parse_xmlPage)

    def parse_xmlPage(self, response):
        print('in parse_xmlPage --- ---','---'*10,upper_path)
        all_file = response.xpath('//li[@class="file"]/a')
        for elem in all_file:
            tmp_url = elem.xpath('@href').extract_first()
            file_name = elem.xpath('text()').extract_first()
            #download remote file path
            xml_path = response.urljoin(tmp_url)
            #download target file path
            output_dir = os.path.join(upper_path+'/output','/'.join(tmp_url.split('/')[2:-1]))
            if not os.path.exists(output_dir):
            	os.system('mkdir -p {}'.format(output_dir))
            wget_command = 'wget {} -O {}/{}'.format(xml_path, output_dir, file_name)
            os.system(wget_command)