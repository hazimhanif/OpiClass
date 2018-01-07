#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 14:31:16 2018

@author: hazimhanif
"""

import os
import flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import OpiClass_thread as oct
import OpiClass_globals as ocg
import time


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/sendURL', methods=['POST'])
def result():
    ocg.thread_id+=1
    ocg.progress_list[ocg.thread_id]=0
    current_thread = ocg.thread_id
    oct.init(ocg.thread_id,request.form['url'])
    time.sleep(0.5)
    while(ocg.progress_list[current_thread]<100):
        print(ocg.progress_list)
        time.sleep(1)
    return redirect(url_for('home'))


def main():
    print("Starting webserver...")
    ocg.init()
    app.secret_key = os.urandom(12)
    app.run(host="0.0.0.0",threaded=True)
    
if __name__ == '__main__':
    main()