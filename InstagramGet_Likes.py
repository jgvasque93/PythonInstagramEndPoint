# -*- coding: utf-8 -*-
#
from InstagramAPI import InstagramAPI

import time
import random
import csv
from random import randint
import datetime as dt
import pandas as pd
import sys
import requests
import json

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


        urlScraping='https://www.instagram.com/graphql/query/?query_hash=d5d763b1e2acf209d62d22d184488e57&variables={"shortcode":"codeSHORT","include_reel":true,"first":50,"after":"max_id"}'
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
            full_names=[]
            usernames=[]
            while has_next_page=='true':
                try:
                    url=urlScraping.replace('codeSHORT',media_id).replace('max_id',max_id)
                    print(url)
                    response=session.get(url,headers=head)
                    has_next_page=json.dumps(response.json()['data']['shortcode_media']['edge_liked_by']['page_info']['has_next_page'])
                    if(has_next_page):
                        max_id=json.dumps(response.json()['data']['shortcode_media']['edge_liked_by']['page_info']['end_cursor'])
                        max_id=str(max_id).replace('\"','')
                    likers=response.json()['data']['shortcode_media']['edge_liked_by']['edges']
                    print(len(likers),'len',has_next_page)
                    for like in likers:
                        try:
                            info=str(like['node']['owner']['username'])
                            usernames.append(info)
                        except Exception as e:
                            info=str(like['node']['username'])
                            usernames.append(info)
                except Exception as e:
                    print(e)
                    time.sleep(10)
            print(len(usernames))

            df = pd.DataFrame()   
            df['usernames']=usernames

            df.to_csv(media_id+'liker_.csv',  index=False, sep=',', encoding='utf-8' )
    except Exception as e:
        print("Main Exception: "+str(e))



if __name__ == '__main__':
    username=''
    pwd=''
    posts=['https://www.instagram.com/p/B7yK1lgFS-X/']
    main(username,pwd,posts)