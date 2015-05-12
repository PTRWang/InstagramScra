#InstagramScraper
#Developed with Python 2.X

import gzip
import mechanize
import urllib2
import re
import time
import shutil
import os
from bs4 import BeautifulSoup

#constants
url = 'https://websta.me/n/'
pre = 'https://websta.me'
PATH = "C:/Users/Peter/Documents/Images/"

def getPATH():
	PATH = raw_input()
	
def createBrowser():
	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.set_handle_gzip(True)
	return br
#add way to login or to just scrape username	

class Scraper():
	#constructor
	def __init__(self):
		print ('Enter username')
		self.username = raw_input()
		self.listofURL = []
		self.totalIMG = 0
		
	#total number of imgs
	def getIMG(self):
		website = url + self.username
		browser = createBrowser()
		browser.open(website)
		response = browser.response().read()
		soup = BeautifulSoup(response)
		new = re.findall('<span class="counts_media">"?\'?([^"\'</span>]*)', str(soup))
		try:
			number = int(new[0])
		except:
			print('User is private')
		return number

	#getting url for image to be downloaded
	def realURL(self, paste):
		browser = createBrowser()
		browser.open(paste)
		response = browser.response().read()
		soup = BeautifulSoup(response)
		text_file = open(PATH + "correct.txt", "w")
		text_file.write(str(soup))
		text_file.close()
		new = re.findall('<a class="mainimg cb_ajax" href="?\'?([^"\'"">]*)', str(soup))
		if len(new) == 0:
			new = re.findall('<div class="jp-jplayer" data-m4v="?\'?([^"\'"]*)', str(soup))
		return new[0]

	#getting a list of the urls to be dwonloaded
	def grabURL(self):
		browser = createBrowser()
		self.totalImg = self.getIMG()
		buffer = True
		website = url + self.username
		print ('Grabbing Image URLs...\n')
		a = 1
		while (buffer):
			browser.open(website)	
			response = browser.response().read()
			soup = BeautifulSoup(response)
			soup = soup.prettify().encode('utf-8')
			list = re.findall('<a class="mainimg" href="?\'?([^"\'>]*)', str(soup)) #list of links on the screen
			a+= 1
			j = 1
			for i in list:
				#print j
				paste = pre + i
				try:
					link = self.realURL(paste)
					self.listofURL.append(link)
				except: 
					num = a * 20 + j
					print'Unable to get photo ' + str(num)
				j += 1
			try:
				result = re.search('a href="(.*)" rel="next"', str(soup))
				website = pre + result.group(1)
				continue
			except:
				buffer = False
				break
	
	def download(self):
		dir = PATH + self.username
		print ('creating ' + dir + ' directory')
		if os.path.exists(dir):
			shutil.rmtree(dir)
		os.mkdir(dir)
		a = 0
		print ('downloading images..')
		for i in self.listofURL:
			a += 1
			if i[-3:] == 'jpg':
				f = open(dir + "/" + self.username + str(a) + '.jpg', 'wb')
				f.write(urllib2.urlopen(i).read())
				f.close()
			else:
				f = open(dir + "/" + self.username + str(a) + '.mp4', 'wb')
				f.write(urllib2.urlopen(i).read())
				f.close()
		print('Done')
				

def main():
	check = Scraper()
	check.grabURL()
	check.download()

main()