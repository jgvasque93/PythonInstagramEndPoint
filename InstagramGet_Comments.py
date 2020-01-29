# -*- coding: utf-8 -*-
#
from InstagramAPI import InstagramAPI
from datetime import datetime,timedelta

import time
import random
from random import randint
import datetime as dt
import pandas as pd
import sys
import requests
import json
import codecs
import unicodedata
import re
import emoji
emoji_pattern = re.compile(
    u"(\ud83d[\ude00-\ude4f])|"  # emoticons
    u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
    u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
    u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
    u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
    "+", flags=re.UNICODE)
def remove_accents(input_str):
    nfkd_form=unicodedata.normalize('NFKD', input_str)
    only_ascii=nfkd_form.encode('ASCII', 'ignore')
    return only_ascii
def loginInstagram(usernameD,paswordD):
    baseUrl='https://www.instagram.com/'
    loginUrl=baseUrl+'accounts/login/ajax/'
    username=usernameD
    pasword=paswordD
    session = requests.Session()
    head = {'Content-type':'application/json','Accept':'application/json'}
    userAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
    session.headers={'user-agent':userAgent}
    session.headers.update({'Referer':baseUrl})
    req=session.get(baseUrl)
    session.headers.update({'X-CSRFToken':req.cookies['csrftoken']})
    login_data={'username':username,'password':pasword}
    login=session.post(loginUrl,data=login_data,allow_redirects=True)
    session.headers.update({'X-CSRFToken':login.cookies['csrftoken']})
    cookies=login.cookies
    return session,head

def main(username,pwd,posts):
    session,head=loginInstagram(username,pwd)
    try:


        urlScraping='https://www.instagram.com/graphql/query/?query_hash=33ba35852cb50da46f5b5e889df7d159&variables={"shortcode":"codeSHORT","include_reel":true,"first":50,"after":"max_id"}'
        for row in posts:
            url = row
            print("url: "+str(url))
            media_id=url.split('/')[-1]
            if(media_id==''):media_id=url.split('/')[-2]
            m = randint(1,4)
            time.sleep(m) 
            print("shorcode: "+str(media_id))
            max_id = ''
            has_next_page = 'true'
            usernames=[]
            text=[]
            dates=[]
            while has_next_page=='true':
                try:
                    url=urlScraping.replace('codeSHORT',media_id).replace('max_id',max_id)
                    print(url)
                    response=session.get(url,headers=head)
                    has_next_page=json.dumps(response.json()['data']['shortcode_media']['edge_media_to_comment']['page_info']['has_next_page'])
                    if(has_next_page):
                        max_id=json.dumps(response.json()['data']['shortcode_media']['edge_media_to_comment']['page_info']['end_cursor'])
                        max_id=str(max_id).replace('\"','')
                    comments_=response.json()['data']['shortcode_media']['edge_media_to_comment']['edges']
                    print(len(comments_),'len',has_next_page)
                    for comment in comments_:
                        try:
                            info=str(comment['node']['owner']['username'])
                            usernames.append(info)
                        except Exception as e:
                            info=str(comment['node']['username'])
                            usernames.append(info)
                        try:
                            info=comment['node']['owner']['text']
                            info= remove_accents(info)                             
                            info=emoji_pattern.sub(r'', info)
                            info= info.replace(',', '').replace(';', ' ')
                            info= info.replace("\n", "").replace("\r", "")
                            text.append(info)
                        except Exception as e:
                            info=comment['node']['text']
                            info= remove_accents(info)                             
                            info=emoji_pattern.sub(r'', info)
                            info= info.replace(',', '').replace(';', ' ')
                            info= info.replace("\n", "").replace("\r", "")
                            text.append(info)
                        try:
                            info=str(comment['node']['owner']['created_at'])
                            dates.append(datetime.utcfromtimestamp(int(info)).strftime('%Y-%m-%d %H:%M:%S'))
                        except Exception as e:
                            info=str(comment['node']['created_at'])
                            dates.append(datetime.utcfromtimestamp(int(info)).strftime('%Y-%m-%d %H:%M:%S'))
                except Exception as e:
                    print(e)
                    time.sleep(10)
            print(len(usernames))

            df = pd.DataFrame()   
            df['usernames']=usernames
            df['text']=text
            df['date']=dates

            df.to_csv(media_id+'comments_.csv',  index=False, sep=';', encoding='utf-8' )
    except Exception as e:
        print("Main Exception: "+str(e))



if __name__ == '__main__':
    username=''
    pwd=''
    posts=['https://www.instagram.com/p/B7yK1lgFS-X/']
    main(username,pwd,posts)