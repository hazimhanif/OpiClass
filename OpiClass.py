#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 14:31:16 2018

@author: hazimhanif
"""
wdir=('/home/hazim/OpiClass')

import OpiClass_thread as oct
import OpiClass_globals as ocg
import flask
import json
import codecs
import pandas as pd
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask import Flask, render_template, send_file
ocg.init()

import logging
import sys
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',datefmt='%d-%m-%Y:%H:%M:%S',stream=sys.stdout, level=logging.DEBUG)

global connected_thread
connected_thread=[0]


@ocg.app.route('/')
def home():
    return render_template('index.html',prog_list=ocg.progress_list)
    
@ocg.app.route('/results')
def results():
    print(ocg.app_list)
    filename="data/web_preview/%s.json"%(ocg.app_list[ocg.thread_id])
    ds=pd.read_json(filename,encoding="utf-8")
    dsnew=ds.loc[1:,["revAuthor","revDate","revRating","revTitle","revText","predicted"]].values.tolist()
    appinfo = ds.loc[1,["appTitle","appPrice","appScore"]].values.tolist()
    appinfo.append(len(ds[ds['predicted']=="Spam"]))
    return render_template('results.html',appid = ocg.app_list[ocg.thread_id],ds=dsnew,info=appinfo)

@ocg.app.route('/processing',  methods=['POST'])
def processing():
    try:
        ocg.thread_id+=1
        ocg.app_list[ocg.thread_id]= request.form['url'].split(sep="=")[1]
    except:
        ocg.thread_id-=1
        return redirect(url_for('home'))
    
    ocg.progress_list[ocg.thread_id]=0
    current_thread = ocg.thread_id
    #oct.init(ocg.thread_id,ocg.app_list[ocg.thread_id])
    return render_template('processing.html',current_thread=current_thread)

@ocg.app.route('/download', methods=['POST'])
def download_file():
    try:
        longstring=request.form['Submit']
        filename='%s.csv'%(longstring.split(sep=" ")[3])
        filepath='/home/hazim/OpiClass/data/dataset/%s'%(filename)
        return send_file(filepath,attachment_filename=filename,as_attachment=True)
    except Exception as e:
        return str(e)

@ocg.socketio.on('connect')
def client_connected():
    global connected_thread
    if ocg.thread_id in connected_thread:
        return
    else:
        connected_thread.append(ocg.thread_id)
        print('Client connected')
        oct.init(ocg.thread_id,ocg.app_list[ocg.thread_id])

@ocg.app.route('/.well-known/acme-challenge/<token_value>')
def letsencrpyt(tmp):
    with open('.well-known/acme-challenge/{}'.format(token_value)) as f:
        answer = f.readline().strip()
    return answer


def main():
    print("Starting webserver...")
    ocg.socketio.run(ocg.app,host='127.0.0.1',port=5000)
    
if __name__ == '__main__':
    main()

#test url
#'https://play.google.com/store/apps/details?id=air.com.hypah.io.slither'  
