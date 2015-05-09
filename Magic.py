from lxml import html
import requests
import sys
import gzip
import mechanize
import urllib2
import re
import time
import shutil
import os
from bs4 import BeautifulSoup
from selenium import webdriver
import StringIO
#import selenium

url = 'https://websta.me/n/'
pre = 'https://websta.me'
PATH = "C:/Users/Peter/Documents/Images/"

def getPATH():
	path = raw_input()
	
def createBrowser():
	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.set_handle_gzip(True)
	return br

def img(url):
	response = urllib2.urlopen(url)
	countsCode = re.search(r'counts\":{\"media\":\d+', response.read())
	count = re.findall(r'\d+', countsCode.group())
	return count[0]

def searchBUTTON(url):
	browser = createBrowser()
	browser.open(url)
	response = browser.response().read()
	soup = BeautifulSoup(response)
	text_file = open(PATH + "out.txt", "w")
	text_file.write(str(soup))
	text_file.close()

#total number of imgs
def getIMG(username):
	website = url + username
	browser = createBrowser()
	browser.open(website)
	response = browser.response().read()
	soup = BeautifulSoup(response)
	text_file = open(PATH + "correct.txt", "w")
	text_file.write(str(soup))
	text_file.close()
	#soup = soup.prettify().encode('utf-8')
	photo = soup.find('span', {'class':"counts_media"})
	new = re.findall('<span class="counts_media">"?\'?([^"\'</span>]*)', str(soup))
	number = int(new[0])
	return number

#getting url for image to be downloaded
def realURL(paste):
	browser = createBrowser()
	browser.open(paste)
	response = browser.response().read()
	soup = BeautifulSoup(response)
	#text_file = open(PATH + "correct.txt", "w")
	#text_file.write(str(soup))
	#text_file.close()
	final = soup.find('a', {'class':"mainimg cb_ajax"})
	new = re.findall('<a class="mainimg cb_ajax" href="?\'?([^"\'"">]*)', str(soup))
	if len(new) == 0:
		new = re.findall('<div class="jp-jplayer" data-m4v="?\'?([^"\'"]*)', str(soup))
	return new[0]
		

#getting a list of the urls to be dwonloaded
def grabURL(username):
	listofURL = []
	imgNum = getIMG(username)
	buffer = True
	website = url + username
	browser = createBrowser()
	a = 1
	while (buffer):
		print str(a) + "\n"
		browser.open(website)
		#for link in browser.links():
		#	print link.text
		response = browser.response().read()
		soup = BeautifulSoup(response)
		soup = soup.prettify().encode('utf-8')
		#links = soup.findAll('script', {'type': 'text/javascript'})
		#text_file = open(PATH + "correct.txt", "w")
		#text_file.write(str(soup))
		#text_file.close()
		list = re.findall('<a class="mainimg" href="?\'?([^"\'>]*)', str(soup)) #list of links on the screen
		#list = re.findall('standard_resolution":{ "?\'?([^"\'>]*)', links)
		#print len(list)
		#a = 1
		for i in list:
			print j
			paste = pre + i
			link = realURL(paste)
			listofURL.append(link)
			j += 1
		a += 1
		try:
			result = re.search('a href="(.*)" rel="next"', str(soup))
			website = pre + result.group(1)
			continue
		except:
			buffer = False
			break
	download(listofURL, username)
		#i = i.replace('\\', '')
		#f = open(PATH + username + str(a) + '.jpg', 'wb')
		#f.write(urllib2.urlopen(i).read())
		#f.close()
		#a += 1
	# a href="/n/privatekanye/?npk=730142692925520174_318472829" rel="next">

def download(list, username):
	dir = PATH + username
	print dir
	if os.path.exists(dir):
		shutil.rmtree(dir)
	os.mkdir(dir)
	a = 0
	for i in list:
		a += 1
		if i[-3:] == 'jpg':
			print i[-3:]
			f = open(dir + "/" + username + str(a) + '.jpg', 'wb')
			f.write(urllib2.urlopen(i).read())
			f.close()
		else:
			f = open(dir + "/" + username + str(a) + '.mp4', 'wb')
			f.write(urllib2.urlopen(i).read())
			f.close()
			
			


#realURL('http://websta.me/p/670314358532487640_318472829')
grabURL('bluntsnbarbells')
#seleniumIMP(url + 'privatekanye')




