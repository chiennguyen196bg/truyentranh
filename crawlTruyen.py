# -*- coding: utf-8 -*-
import requests
from lxml import html
import time
#from slugify import slugify
import json
import pymongo
from pymongo import MongoClient

import unicodedata,re

def slugify(str):
    slug = unicodedata.normalize("NFKD",unicode(str)).encode("ascii", "ignore")
    slug = re.sub(r"[^\w]+", " ", slug)
    slug = "-".join(slug.lower().strip().split())
    return slug

import mech
ab = mech.anonBrowser(proxies=[],\
			user_agents=[('user_agent', 'superSecretBroser')])
	
# db = get_db()
client = MongoClient('mongodb://localhost:27017/')
db = client.admin
# add document

def crawl_chapter(url):
	"""Lay noi dung chap"""
	try:
		# response = ano.open(url)
		response = requests.get(url)
	except:
		f = open('public/urlerr.txt','a',0)
		f.write(url+'\n')
		f.close()
	else:
		if response.status_code == 200: # Response Code  
			chap = {}
			parsed_body = html.fromstring(response.text)
			# lay tieu de
			word = parsed_body.xpath('//div[@class="box lam-nham-chap lam-nham-chap-2 entry-content"]/h1/text()')
			chap['name'] = word[0]
			chap['slug'] = slugify(chap['name'])
			chap['_id'] = time.time()
			#lay noi dung
			chap['content'] = parsed_body.xpath('//div[@class="image-chap entry-content"]/img/@src')
			db.chap.insert_one(chap)
			return (chap['name'], chap['_id'], chap['slug'])
		else:
			print "Error:", url

def crawl_title(url):
	try:
		# response = ano.open(url)
		response = requests.get(url)
	except:
		f = open('urlerr.txt','a',0)
		f.write(url+'\n')
		f.close()
	else:
		if response.status_code == 200: # Response Code  
			item = {}
			parsed_body = html.fromstring(response.text)
			
			item['name'] = parsed_body.xpath('//div[@class="hentry"]/ul/li[2]/h1/text()')
			if item['name'] == []:
				item['name'] = 'null'
			else:
				item['name'] = item['name'][0]
			item['slug'] = slugify(item['name'])
			# lay img thumb
			item['thumb'] = parsed_body.xpath('//div[@class="hentry"]/ul/li[1]/div/img/@src')[0]
			try:
				imgData = ab.open(item['thumb']).read()
			except:
				f = open('public/urlerrthumb.txt','a',0)
				try:
					f.write(item['thumb']+'\n')
				except:
					print "thumb img err"
				f.close()
			else:
				f = open('public/images/'+item['slug']+'.jpg', 'wb')
				f.write(imgData)
				f.close()

			item['author'] = parsed_body.xpath('//div[@class="hentry"]/ul/li[3]/span/a/text()')
			item['genres'] = parsed_body.xpath('//div[@class="hentry"]/ul/li[5]/a/text()')
			item['status'] = parsed_body.xpath('//div[@class="hentry"]/ul/li[6]/a/text()')[0]
			item['summary'] = parsed_body.xpath('/html/head/meta[10]/@content')[0]
			if(item['summary'].find('Truyentranhmoi.com') != -1):
				item['summary'] = ''
			item['chapter'] = []
			list_chap = parsed_body.xpath('//div[@class="box chap-list"]/ul/li/a/@href')
			list_chap = list_chap[::-1]
			for urlchap in list_chap:
				(chap_name, chap_id, chap_slug) = crawl_chapter(urlchap)
				chap = {'name': chap_name, 'id': chap_id, 'slug': chap_slug}
				item['chapter'].append(chap)
			item['lastChap'] = item['chapter'][len(item['chapter'])-1]
			return db.truyen.insert_one(item).inserted_id
			
		else:
			print "Error:", url


if __name__ == '__main__':
	# url = 'http://truyentranhmoi.com/the-god-of-high-school-chap-214/'
	# chap = crawl_chapter(url)
	# print chap.title

	url = 'http://truyentranhmoi.com/midara-na-ao-chan-wa-benkyou-ga-dekinai/'
	info = crawl_title(url)
	print info

