#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 09:22:03 2018

@author: hazimhanif
"""
import subprocess



def start(appid):
    print("======Starting Modeller=======")
    command = '/usr/local/bin/Rscript'
    arg = '--vanilla'
    path2script = '/Volumes/Extended/OneDrive/Documents/FSKTM/Master (Sentiment Analysis)/Thesis/OpiClass/r_scripts/playstore.R'
    subprocess.call([command, arg, path2script, appid])
    print("======Finish prediction=====")
     

    