#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 01:23:28 2018

@author: hazimhanif
"""

import threading
import time
import OpiClass_globals as ocg
import OpiClass_scraper as ocs
import OpiClass_filter as ocf


exitFlag = 0

class myThread (threading.Thread):
   def __init__(self, threadID, counter,url):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.counter = counter
      self.url = url
      
   def run(self):
      print("Starting ThreadID-" + str(self.threadID) + ". Processing: "+self.url)
      print_time(self.threadID, 5, self.counter,self.url)
      print("Exiting " + str(self.threadID))

def print_time(threadID, counter, delay, url):
   while counter:
      if exitFlag:
         threadID.exit()
      time.sleep(delay)
      ##print("ThreadID-%s: %s" % (threadID, time.ctime(time.time())))
      ocg.progress_list[threadID]+=20
      appid=url.split(sep="=")[1]
      ocs.main(appid)
      ocf.main(appid)
      ocg.socketio.emit('updateVal', {'progress_list': ocg.progress_list} , broadcast=False)
      #print(ocg.progress_list)
      counter -= 1


def init(thread_id,url):
    # Create new threads
    
    myThread(ocg.thread_id, 1,url).start()
    