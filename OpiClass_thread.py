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
import time


exitFlag = 0

class myThread (threading.Thread):
   def __init__(self, threadID,name,appid):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.appid = appid
      
   def run(self):
      print("Starting " + self.name + ". Processing: "+self.appid)
      print_time(self.name,self.threadID,self.appid)
      print("Exiting " + str(self.threadID))

def print_time(threadName,threadID,threadappid):
      file2 = "%s.json"%(threadappid)
      if file2 not in os.listdir("data/web_preview"):
          msg='Initiate request for %s' % (threadappid)
          ocg.progress_list[threadID]+=5
          ocg.socketio.emit('updateVal', {'progress_list': ocg.progress_list, 'text':msg} , broadcast=False)
          ocs.start(threadappid,threadID)
          ocf.start(threadappid,threadID)
          ocm.start(threadappid,threadID)
      else:
          print("File already exist")
          msg='File already exist for %s. Proceeding.' % (threadappid)
          ocg.progress_list[threadID]=100
          ocg.socketio.emit('updateVal', {'progress_list': ocg.progress_list, 'text':msg} , broadcast=False)


def init(thread_id,appid):
    # Create new threads
    myname = "Thread of %s"% str(ocg.thread_id)
    myThread(ocg.thread_id,myname,appid).start()
    