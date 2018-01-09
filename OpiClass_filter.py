# -*- coding: utf-8 -*-

'''
Created on 13 Dec 2016

@author: Hazim Hanif
'''
import os
import codecs
import json
import re
import OpiClass_globals as ocg

global wordList
global indonList
global finalList
global english_count
global indon_count
global total_count
global drop_count
global total_apps

total_apps=0
english_count=0
indon_count=0
total_count=0
drop_count=0
finalList=[]
revDir="data/reviews/"
dictDir="data/dict/"
filteredDir="data/filtered_reviews/"

def saveFilteredReviews(data,file):
    filename = filteredDir+file
    try:
        with codecs.open(filename, 'wb','utf-8') as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True, separators=(',', ':'),ensure_ascii=False)
    except Exception as e:
        print(e)

def isIndon(wordIndo):
    
    if wordIndo in map(str.lower,[x.strip("\r\n\t") for x in indonList]):
            #print("Indo: "+wordIndo)
            return 1            
    return 0

def isEnglish(wordEng):
    
    if wordEng in map(str.lower,[x.strip("\r\n\t") for x in wordList]):
            #print("English: "+wordEnglish)
            return 1            
    return 0

    
def getReviews(data,threadID,appid):
    global english_count
    global indon_count
    global total_count
    global drop_count
    checkcount=0
    i=0
    
    size_data = len(data)
    division=int(size_data/30)
    checkcount+=division
    print("Total review:"+ str(size_data))
    while i < size_data:
        #print(i)
        if i==checkcount and ocg.progress_list[threadID]<85:
            ocg.progress_list[threadID]+=division
            msg='Filtering opinions for %s. Please sit back, relax and have a coffee  ☕️' % (appid)
            ocg.socketio.emit('updateVal', {'progress_list': ocg.progress_list, 'text':msg} , broadcast=False)
            checkcount+=division
            
        countEnglish_perRev=0
        countIndon_perRev=0
        words=str(data[i]['revText']).strip(".,!?:;`~@#$%^&*()-+=*'[]{}|\"/<>")
        words= re.sub("\."," ",words)
        words= re.sub("\,"," ",words)
        words= re.sub("  "," ",words)
        words= re.sub("   "," ",words)
        words=words.lower()
        words_split=words.split(sep=" ")

        for word in words_split:
            countEnglish_perRev=countEnglish_perRev+isEnglish(word)
            countIndon_perRev=countIndon_perRev+isIndon(word)
        
        if countEnglish_perRev == len(words_split):
            #print("English: "+words)
            english_count=english_count+1
            drop_count=drop_count+1
            del data[i]
            size_data=size_data-1
            continue
          
        if countIndon_perRev > (len(words_split)/2):
            #print("Endon: "+words)
            indon_count=indon_count+1
            drop_count=drop_count+1
            del data[i]
            size_data=size_data-1
            continue
        
        data[i]['revText']=words
        total_count=total_count+1
        i=i+1
    return(data)
        
def openFile(file):
    filename=revDir+file
    with codecs.open(filename,'rb','utf-8') as data_file:    
        return(json.load(data_file))

def loadWordList():
    global wordList
    global indonList
    indonList=[]
    wordList=[]
    
    data=codecs.open("data/dict/english.txt",'rb','utf-8')  
    wordList=data.readlines()   
    data=codecs.open("data/dict/indon.txt",'rb','utf-8')    
    indonList=data.readlines()   
        
def start(appid,threadID):
    print("======Starting Filtering=======")
    msg='Initiate filtering for %s' % (appid)
    ocg.progress_list[threadID]+=2
    ocg.socketio.emit('updateVal', {'progress_list': ocg.progress_list, 'text':msg} , broadcast=False)
    file="%s.json" % (appid)
    loadWordList()
    data=openFile(file)
    data=getReviews(data,threadID,appid)
    saveFilteredReviews(data,file)
    if ocg.progress_list[threadID]!=85:
        ocg.progress_list[threadID]+=(85-ocg.progress_list[threadID])
    
    msg='Finished filtering for %s' % (appid)
    ocg.socketio.emit('updateVal', {'progress_list': ocg.progress_list, 'text':msg} , broadcast=False)
    print("======Finish Filtering=======")
    