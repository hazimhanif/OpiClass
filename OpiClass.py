#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 14:31:16 2018

@author: hazimhanif
"""

import os
import flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
    

def main():
    print("Starting webserver...")
    app.secret_key = os.urandom(12)
    app.run(host="0.0.0.0")
    
if __name__ == '__main__':
    main()