#!/usr/bin/python
#-*- coding: utf-8 -*-

#===========================================================
# File Name: CRI_BeijingHour.py
# Author：Sha0hua
# E-mail:sha0hua@foxmail.com
# Created Date: 2017-01-11
# Modified Date: 2017-01-11
# Version: 2.0
# Description: Added progess bar while downloading
#===========================================================
import re
import urllib
import urllib2
import os
import time
import cookielib
import HTMLParser
import shutil

def mycopytree(src,dst):
    _orig_copystat = shutil.copystat
    shutil.copystat = lambda x, y: x
    shutil.copytree(src, dst)
    shutil.copystat = _orig_copystat

if os.path.exists('c:/Python27/Lib/site-packages/progressbar/'):
    pass
else:
    mycopytree('./4install/python-progressbar-master/progressbar','c:/Python27/Lib/site-packages/progressbar/')

if os.path.exists('c:/Python27/Lib/site-packages/bs4/'):
    pass
else:
    mycopytree('./4install/beautifulsoup4-4.3.2/bs4','c:/Python27/Lib/site-packages/bs4/')


from progressbar import *
#from bs4 import BeautifulSoup
class SciA():
    url = ''
    def __init__(self, url):
        self.url = url

    def getLink(self):
        url = self.url
        page = urllib.urlopen(url)
        html = page.read()
        path_tmp = './tmp.txt'
        reg = r"<a href='(.*?)'>The Beijing Hour"
        link_re = re.compile(reg)

        link_list = re.findall(link_re,html)   #List all newspage link
        newspage = "http://english.cri.cn"+str(link_list[0])
        
        return newspage
        #print newspage

    def getMp3(self):
        print "analyzing..."
        url = self.getLink()
        page = urllib.urlopen(url)
        html = page.read()
#        print html
#        reg = r'<a id="mp3Link" href="(.*?)"'
        reg = r'<A href="(.*?.mp3)">'

        Mp3_re = re.compile(reg)
        Mp3_list = re.findall(Mp3_re,html)   #Find all mp3 link     
        Mp3_link = str(Mp3_list[0])   
        Mp3_name = "20"+Mp3_link.split("/")[6]
        #print Mp3_name

#Download mp3(with progress bar):            
        mp3_path='.\%s'%Mp3_name

        widgets = ['downloading...', Percentage(), ' ', Bar(marker=RotatingMarker()), ' ', ETA(), ' ', FileTransferSpeed()]
        pbar = ProgressBar(widgets=widgets)        

        def dlProgress(count, blockSize, totalSize):
            if pbar.maxval is None:
                pbar.maxval = totalSize
                pbar.start()
            pbar.update(min(count*blockSize, totalSize))

        if os.path.exists(mp3_path):
            print "no update"
        else:
            urllib.urlretrieve(Mp3_link,mp3_path,reporthook=dlProgress)   #Downlad mp3
            pbar.finish()

if __name__ == '__main__':
    print "\nHi, this is Shaohua, the writer of this script, thanks for using it. If there's any problem plz send me email: cell.fantasy@qq.com. Enjoy Learning!\n"

    File = SciA("http://english.cri.cn/easyfm/hour.html")
    File.getLink()
    File.getMp3()
    
    print "\ndone"
    time.sleep(3)
