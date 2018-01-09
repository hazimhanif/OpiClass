#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 09:22:03 2018

@author: hazimhanif
"""
import subprocess
import OpiClass_globals as ocg
import os

def start(appid,threadID):
    print("======Starting Modeller=======")
    msg='Initiate features extraction & prediction for %s' % (appid)
    ocg.progress_list[threadID]+=10
    ocg.socketio.emit('updateVal', {'progress_list': ocg.progress_list, 'text':msg} , broadcast=False)
    command = '/usr/local/bin/Rscript'
    arg = '--vanilla'
    path2script = '/Volumes/Extended/OneDrive/Documents/FSKTM/Master (Sentiment Analysis)/Thesis/OpiClass/r_scripts/playstore.R'
    try:
        subprocess.call([command, arg, path2script, appid])
    except:
        print("exception")
        
    file2 = "%s.json"%(appid)
    while file2 not in os.listdir("data/web_preview"):
        continue
    
    msg='Finished features extraction & prediction for %s' % (appid)
    ocg.progress_list[threadID]=100
    ocg.socketio.emit('updateVal', {'progress_list': ocg.progress_list, 'text':msg} , broadcast=False)
    print("Finish prediction")
    return
    

    