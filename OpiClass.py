#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 14:31:16 2018

@author: hazimhanif
"""

import os

import OpiClass_thread as oct
import OpiClass_globals as ocg
import time
import flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask import Flask, render_template
ocg.init()

@ocg.app.route('/')
def home():
    return render_template('index.html',prog_list=ocg.progress_list)
    
@ocg.app.route('/other')
def other():
    return redirect(url_for('home', _anchor='detection'))
    

@ocg.app.route('/processing', methods=['POST'])
def processing():
    ocg.thread_id+=1
    ocg.progress_list[ocg.thread_id]=0
    ocg.counter[ocg.thread_id]=0
    current_thread = ocg.thread_id
    oct.init(ocg.thread_id,request.form['url'])
    return render_template('processing.html',current_thread=current_thread)

@ocg.socketio.on('connect')
def client_connected():
    print('Client connected')

def main():
    print("Starting webserver...")
    ocg.socketio.run(ocg.app)
    
if __name__ == '__main__':
    main()
