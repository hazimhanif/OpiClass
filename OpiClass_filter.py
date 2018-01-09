# -*- coding: utf-8 -*-

'''
Created on 13 Dec 2016

@author: Hazim Hanif
'''
import os
import codecs
import json
import re

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

    
def getReviews(data):
    global english_count
    global indon_count
    global total_count
    global drop_count
    i=0
    size_data = len(data)
    print("Total review:"+ str(size_data))
    while i < size_data:
        print(i)
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
        
def start(appid):
    print("======Starting Filtering=======")
    file="%s.json" % (appid)
    loadWordList()
    data=openFile(file)
    data=getReviews(data)
    saveFilteredReviews(data,file)
    print("======Finish Filtering=======")
    