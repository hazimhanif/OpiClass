#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 01:23:28 2018

@author: hazimhanif
"""

import threading
import OpiClass_globals as ocg
import OpiClass_scraper as ocs
import OpiClass_filter as ocf
import OpiClass_model as ocm
import os


exitFlag = 0

class myThread (threading.Thread):
   def __init__(self, threadID,name,url):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.url = url
      
   def run(self):
      print("Starting " + self.name + ". Processing: "+self.url)
      print_time(self.name,self.threadID,self.url)
      print("Exiting " + str(self.threadID))

def print_time(threadName,threadID,threadUrl):
      appid=ocg.app_list[threadID]
      file2 = "%s.json"%(appid)
      if file2 not in os.listdir("data/web_preview"):
          msg='Initiate request for %s' % (appid)
          ocg.progress_list[threadID]+=5
          ocg.socketio.emit('updateVal', {'progress_list': ocg.progress_list, 'text':msg} , broadcast=False)
          ocs.start(appid,threadID)
          ocf.start(appid,threadID)
          ocm.start(appid,threadID)
      else:
          print("File already exist")
          msg='File already exist for %s. Proceeding.' % (appid)
          ocg.progress_list[threadID]=100
          ocg.socketio.emit('updateVal', {'progress_list': ocg.progress_list, 'text':msg} , broadcast=False)
          
      return


def init(thread_id,url):
    # Create new threads
    myname = "Thread of %s"% str(ocg.thread_id)
    myThread(ocg.thread_id,myname,url).start()
    