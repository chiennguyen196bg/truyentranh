# -*- coding: utf-8 -*-
import requests
from lxml import html


def crawl_list_urls(url):

	response = requests.get(url)

	# Response
	if response.status_code == 200: # Response Code  
		parsed_body = html.fromstring(response.text)
		list_urls = parsed_body.xpath('//div[@class="box chap-list truyen-list"]/ul/li/a[2]/@href')

		# print list_urls
		return list_urls
	# print parsed_body
	

	

if __name__ == '__main__':
	url = 'http://truyentranhmoi.com/danh-sach/page/2/'
	lis = crawl_list_urls(url)
	print lis