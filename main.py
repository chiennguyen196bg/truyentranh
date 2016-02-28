# -*- coding: utf-8 -*-
import requests
from lxml import html
import json
import pymongo
from pymongo import MongoClient
import time
from crawlTruyen import crawl_title
from crawlList import crawl_list_urls


	
# db = get_db()
client = MongoClient('mongodb://localhost:27017/')
db = client.test

for i in range(1,54):
	urlList = 'http://truyentranhmoi.com/danh-sach/page/%d/' % i
	listUrlPage = crawl_list_urls(urlList)
	print i
	for url in listUrlPage:
		info = crawl_title(url)
		print info
		
		
print "Done"

