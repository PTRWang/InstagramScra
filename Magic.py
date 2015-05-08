from lxml import html
import requests
import sys
import gzip
import mechanize
import urllib2
import re
from bs4 import BeautifulSoup
from selenium import webdriver

url = 'https://instagram.com/'
PATH = "C:\Users\Peter\Documents\Images\\"
load = 'div.mbMedia > div.ResponsiveBlock > button > span'

def getPATH():
	path = raw_input()
	
def createBrowser():
	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.set_handle_gzip(True)
	return br

def searchBUTTON(url):
	browser = createBrowser()
	browser.open(url)
	response = browser.response().read()
	soup = BeautifulSoup(response)
	text_file = open(PATH + "out.txt", "w")
	text_file.write(str(soup))
	text_file.close()
	
def seleniumIMP(url):
	driver = webdriver.Firefox()
	driver.get(url)
	element = driver.find_element_by_xpath("//html/body/span/div/div/div/section/div/span/a/span[2]/span/span")
	element.click()
	#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

	
def grabURL(username):
	website = url + username
	browser = createBrowser()
	browser.open(website)
	for link in browser.links():
		print link.text
	response = browser.response().read()
	soup = BeautifulSoup(response)
	#soup = soup.prettify().encode('utf-8')
	links = soup.findAll('script', {'type': 'text/javascript'})
	text_file = open(PATH + "out.txt", "w")
	text_file.write(str(links))
	text_file.close()
	list = re.findall('standard_resolution":{"url":":?\'?([^"\']*)', str(links))
	#list = re.findall('standard_resolution":{ "?\'?([^"\'>]*)', links)
	print len(list)
	a = 1
	for i in list:
		i = i.replace('\\', '')
		f = open(PATH + username + str(a) + '.jpg', 'wb')
		f.write(urllib2.urlopen(i).read())
		f.close()
		a += 1

grabURL('shadrinov')
#seleniumIMP(url + 'privatekanye')