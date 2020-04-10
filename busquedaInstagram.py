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
def getDataframe(valuesSettings):
    df = pd.DataFrame.from_records(valuesSettings)
    new_header = df.iloc[0] #grab the first row for the header
    df = df[1:] #take the data less the header row
    df.columns = new_header #set the header row as the df header
    #df['Division']=df['Division'].str.title()
    return df.reset_index(drop=True)
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
def main(username,pwd,TIPO,PARAMQUERY):
    session,head=loginInstagram(username,pwd)
    try:


        urlScraping='https://www.instagram.com/web/search/topsearch/?context=TIPO&query=PARAMQUERY'
        for rowPARAMQUERY in PARAMQUERY:
            has_next_page = 'true'
            usersARRAY=[]
            hashtagARRAY=[]
            placesARRAY=[]
            try:
                url=urlScraping.replace('PARAMQUERY',rowPARAMQUERY).replace('TIPO',TIPO)
                print(url)
                response=session.get(url,headers=head)
                if(TIPO=='user'):
                    users=response.json()['users']
                    for xusers in users:
                        position=xusers['position']
                        infoUser=xusers['user']
                        pk=infoUser['pk']
                        username=infoUser['username']
                        full_name=infoUser['full_name']
                        usersARRAY.append([position,pk,username,full_name])
                    df = getDataframe([['position','pk','username','full_name']]+usersARRAY)   
                    df.to_csv(TIPO+rowPARAMQUERY+'.csv',  index=False, sep=',', encoding='utf-8' )
                elif(TIPO=='hashtag'):
                    hashtags=response.json()['hashtags']
                    for xhashtags in hashtags:
                        position=xhashtags['position']
                        infohashtag=xhashtags['hashtag']
                        name=infohashtag['name']
                        id=infohashtag['id']
                        media_count=infohashtag['media_count']
                        hashtagARRAY.append([position,name,id,media_count])
                    df = getDataframe([['position','name','id','media_count']]+hashtagARRAY)   
                    df.to_csv(TIPO+rowPARAMQUERY+'.csv',  index=False, sep=',', encoding='utf-8' )
                elif(TIPO=='place'):
                    places=response.json()['places']
                    for xplaces in places:
                        position=xplaces['position']
                        infoplaces=xplaces['place']['location']
                        try:
                            lng=infoplaces['lng']
                        except Exception as e:
                            lng=''
                        try:
                            lat=infoplaces['lat']
                        except Exception as e:
                            lat=''
                        pk=infoplaces['pk']
                        name=infoplaces['name']
                        address=infoplaces['address']
                        city=infoplaces['city']
                        placesARRAY.append([position,pk,lng,lat,name,address,city])
                    df = getDataframe([['position','pk','lng','lat','address','city']]+placesARRAY)   
                    df.to_csv(TIPO+rowPARAMQUERY+'.csv',  index=False, sep=',', encoding='utf-8' )
            except Exception as e:
                print("Main Exception: "+str(e))

    except Exception as e:
        print("Main Exception: "+str(e))



if __name__ == '__main__':
    username=''
    pwd=''
    typo='hashtag'
    queries=['covid2']
    main(username,pwd,typo,queries)
    typo='user'
    queries=['covid']
    main(username,pwd,typo,queries)
    typo='place'
    queries=['guayaquil']
    main(username,pwd,typo,queries)