from BeautifulSoup import BeautifulSoup
import requests
import re
import urllib2
import os
import cv2
import random
import rospkg

def get_soup(url,header):
  return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)))


def download_images(query,image_type,DIR,n):

	query= query.split()
	query='+'.join(query)
	url=url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
	header = {'User-Agent': 'Mozilla/5.0'} 
	soup = get_soup(url,header)

	n1 = len([i for i in os.listdir(DIR) if image_type in i]) + 1

	for eachItem in soup.findAll("img"):
		# eachItem.ul.decompose()
		imgfullLink = eachItem.get('src').strip()
		print imgfullLink

		raw_img = urllib2.urlopen(imgfullLink).read()
		
		cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1

		dirimg = DIR + image_type + "_"+ str(cntr)+".jpg"
		f = open(dirimg, 'wb')
		f.write(raw_img)
		f.close()

		if abs(cntr-n1) >= n:
			break

def delete_images(DIR,image_type,n1,n):
	for i in range(n+1):
		dirimg = DIR + image_type + "_"+ str(n1+i)+".jpg"
		os.remove(dirimg)

#n <=20
def show_image(query,n=1,image_type="All",delete=True):

	rospack = rospkg.RosPack()
	packdir = rospack.get_path('web')

	#Use dir to define the temporal directory of the images
	DIR = packdir+"/imgs/"

	n1 = len([i for i in os.listdir(DIR) if image_type in i]) + 1
	download_images(query,image_type,DIR,n)

	for i in range(n):
		dirimg = DIR + image_type + "_"+ str(n1+i)+".jpg"
		img = cv2.imread(dirimg,1)

		w = random.randint(0, 1000)
		h = random.randint(0, 700)
		cv2.imshow('image '+str(i),img)
		cv2.moveWindow('image '+str(i), w, h)
	cv2.waitKey(0)

	if delete:
		delete_images(DIR,image_type,n1,n)


if __name__ == '__main__':
	show_image("robot bender",6)