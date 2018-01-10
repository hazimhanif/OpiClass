#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 02:26:54 2018

@author: hazimhanif
"""


def init():
    import os
    import flask
    from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
    from flask import Flask, render_template
    from flask_socketio import SocketIO,send,emit
    import eventlet
    import gevent

    global app
    global socketio
    global thread_id
    global progress_list
    global app_list
    
    app = Flask(__name__)
    app.secret_key = os.urandom(12)
    app.config['SERVER_NAME']='opiclass.mylocaltest:5000'
    socketio = SocketIO(app,async_mode='threading',engineio_logger=False)
    
    thread_id=0;
    progress_list={}
    app_list={}
    