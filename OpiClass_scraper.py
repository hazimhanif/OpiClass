# -*- coding: utf-8 -*-

'''
Created on 1 Dec 2016

@author: Hazim Hanif
'''

import requests
import codecs
from lxml import html
import json
from bs4 import BeautifulSoup
import play_scraper


global reviewsCounter
global appsCounter
global skipApp
global currentApps

skipApp=False
reviewsCounter=0
appsCounter=0
def saveRawData(raw_data,appId,pageNum):
    filename = "data/raw/reviews_%s_page_%d.raw" % (appId,pageNum)
    try:
        fopen = codecs.open(filename,"wb","utf-8")
        fopen.write(raw_data)
    except Exception as e:
        print(e)

def sendRequest(appid):
    global skipApp
    
    skipApp=False
    pageN=0
    revList=[]
    
    
    appSingleInfo=play_scraper.details(appid)
    
    
    while(pageN<=1):
        url = "https://play.google.com/store/getreviews"
        pageNum=pageN
        appId=appid
        hl="ms"
        headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
        payload = 'reviewType=0&pageNum=%d&hl=%s&id=%s&reviewSortOrder=2&xhr=1' %(pageNum,hl,appId)
        
        page_text = requests.post(url, data=payload, headers=headers).text[6:]
        js = json.loads(page_text)
        
        if(len(js[0])<3 and pageN==0):
            skipApp=True
            return(revList)
        
        if(len(js[0])<3):
            break
        
        soup = BeautifulSoup(js[0][2],"lxml")
        reviews_div = soup.find_all( 'div', {'class':'single-review'} )
        
        review_date=[]
        review_author=[]
        review_rating=[]
        review_title=[]
        review_text=[]
        for review in reviews_div:
            body = review.find(class_='review-body')
            title = body.find(class_='review-title')
            link = body.find(class_='review-link')
            date = review.find(class_='review-date')
            rating_old = review.find(class_='tiny-star').get('aria-label')
            name = review.find(class_='author-name')
            title_old=title.get_text().strip()
            title.decompose()
            link.decompose()
            text_old = body.get_text().strip()
            date_old = date.get_text()
            name_old = name.get_text().strip()
            
            review_date.append(date_old)
            review_author.append(name_old)
            review_rating.append(rating_old)
            review_title.append(title_old)
            review_text.append(text_old)
        
        if(len(review_rating)==0 and pageN==0):
            skipApp=True
            return(revList)
        
        if(len(review_rating)==0):
            break
        
        saveRawData(js[0][2],appid,pageNum)
        revsPerPage=getReviews(appSingleInfo,review_date,review_text,review_rating,review_author,review_title)
        
        try:
            while(True):
                revList.append(revsPerPage.pop())
        except:
            None
    
        pageN+=1
        
    
    return(revList)
        
    
def getReviews(appSingleInfo,review_date,review_text,review_rating,review_author,review_title):
    global reviewsCounter
    
    rateList={"Dinilaikan 5 bintang daripada lima bintang":5,
              "Dinilaikan 4 bintang daripada lima bintang":4,
              "Dinilaikan 3 bintang daripada lima bintang":3,
              "Dinilaikan 2 bintang daripada lima bintang":2,
              "Dinilaikan 1 bintang daripada lima bintang":1,
              "Dinilaikan 0 bintang daripada lima bintang":0}
    
    c=0
    
    revPerPage=[]
    
    rev_date=""
    rev_author=""
    rev_text=""
    rev_rating=""
    rev_title=""
    
    try:
        while(c < len(review_rating)):
            rev_date=review_date[c]
            rev_author=review_author[c]
            rev_rating=rateList[review_rating[c]]
            rev_title=review_title[c]
            rev_text=review_text[c]
            
            if rev_title==" " or rev_title=="":
                rev_title="NA"
            if rev_text==" " or rev_text=="":
                rev_text="NA"
            if rev_author==" " or rev_author=="":
                rev_author="NA"
    
            revPerPage.append({'appId':appSingleInfo['app_id'],'appTitle':appSingleInfo['title'],'appScore':float(appSingleInfo['score']),'appPrice':float(appSingleInfo['price']),'revDate': rev_date,'revAuthor':rev_author,'revRating':float(rev_rating),'revTitle':rev_title,'revText':rev_text})
            reviewsCounter+=1
            c=c+1
               
    except Exception as e:
        None
    
    return(revPerPage)


def saveRevToFile(appId,revPerApp):
    filename = "data/reviews/%s.json" % (appId)
    try:
        with codecs.open(filename, 'wb','utf-8') as outfile:
            json.dump(revPerApp, outfile, indent=4, sort_keys=True, separators=(',', ':'),ensure_ascii=False)
    except Exception as e:
        print(e)



def start(appid):
    print("======Starting Scraping=======")
    revPerApp=sendRequest(appid)
    saveRevToFile(appid,revPerApp)
    print("======Finish Scrapining=======")
    
#'https://play.google.com/store/apps/details?id=air.com.hypah.io.slither'    