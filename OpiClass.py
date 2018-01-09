#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 14:31:16 2018

@author: hazimhanif
"""
wdir=('/Volumes/Extended/OneDrive/Documents/FSKTM/Master (Sentiment Analysis)/Thesis/OpiClass')

import OpiClass_thread as oct
import OpiClass_globals as ocg
import flask
import json
import codecs
import pandas as pd
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask import Flask, render_template
ocg.init()



@ocg.app.route('/')
def home():
    return render_template('index.html',prog_list=ocg.progress_list)
    
@ocg.app.route('/results')
def results():
    filename="data/web_preview/%s.json"%(ocg.app_list[ocg.thread_id])
    ds=pd.read_json(filename,encoding="utf-8")
    dsnew=ds.loc[1:,["revAuthor","revDate","revRating","revTitle","revText","predicted"]].values.tolist()
    appinfo = ds.loc[1,["appTitle","appPrice","appScore"]].values.tolist()
    appinfo.append(len(ds[ds['predicted']=="Spam"]))
    return render_template('results.html',appid = ocg.app_list[ocg.thread_id],ds=dsnew,info=appinfo)

@ocg.app.route('/processing', methods=['POST'])
def processing():
    ocg.thread_id+=1
    ocg.progress_list[ocg.thread_id]=0
    ocg.app_list[ocg.thread_id]= request.form['url'].split(sep="=")[1]
    current_thread = ocg.thread_id
    #oct.init(ocg.thread_id,request.form['url'])
    return render_template('processing.html',current_thread=current_thread)

@ocg.socketio.on('connect')
def client_connected():
    print('Client connected')
    oct.init(ocg.thread_id,ocg.app_list[ocg.thread_id])

def main():
    print("Starting webserver...")
    ocg.socketio.run(ocg.app)
    
if __name__ == '__main__':
    main()



    
#'https://play.google.com/store/apps/details?id=air.com.hypah.io.slither'  