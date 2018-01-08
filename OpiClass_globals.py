#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 02:26:54 2018

@author: hazimhanif
"""


def init():
    import os
    import json
    import flask
    from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
    from flask import Flask, render_template
    from flask_socketio import SocketIO,send,emit

    global app
    global socketio
    global thread_id
    global progress_list
    global counter
    
    app = Flask(__name__)
    app.secret_key = os.urandom(12)
    socketio = SocketIO(app,port=5000,async_mode='threading',logger=False)
    
    thread_id=0;
    progress_list={}
    counter={}

