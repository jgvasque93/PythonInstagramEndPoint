from InstagramAPI import InstagramAPI
import time
from datetime import datetime
import random
import sys
from random import randint
import pandas as pd
user = 'user'
pwd = 'PASSWORD'
#user_id  = '41864127'
#   user_id  = '25758869'
#user_id='857021616'
def writeCSV(posts,user_id):
    header=[]
    header.append('username')
    header.append('like_count')
    header.append('comment_count')
    header.append('created_at')
    header.append('code_potst')
    header.append('text')
    header.append('profile_pic_url')

    
    data=pd.DataFrame(posts,columns=header)
    data.to_csv(user_id+'.csv', sep=',', encoding='utf-8', index=False)
 
def getTimeline(username,fechatest,API):
    print(username)
    API.searchUsername(username)
    t=API.LastJson
    try:
        if(t['status']!='fail' and not t['user']['is_private']):
            user_id=str(t['user']['pk'])
            posts=[]
            next_max_id = ''
            g = API.getUserFeed(user_id,next_max_id)
            temp = API.LastJson
            if(int(temp['num_results'])>0):
                while 1:
                    try:
                        while g==False:
                            print("wait")
                            n = randint(50,90)
                            time.sleep(3*n)
                            g = API.getUserFeed(user_id,next_max_id)
                            temp = API.LastJson
                        print('reading')
                        for item in temp["items"]:
                            ite=[]
                            ite.append(username)
                            try:
                                ite.append(item['like_count'])
                            except Exception as e:
                                ite.append(0)
                            try:
                                ite.append(item['comment_count'])
                            except Exception as e:
                                ite.append(0)

                            ts=int(item['taken_at'])
                            fecha=datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                            ite.append(fecha)
                            ite.append(str(item['code']))

                            try:
                                texto=item['caption']['text'].replace(',',' ').replace('\t',' ').replace('\r',' ').replace('\n',' ').replace('\"',' ')
                                ite.append(texto)
                            except Exception as e:
                                ite.append('')
                            try:
                                profile_pic_id=item['image_versions2']['candidates'][0]['url']
                                ite.append(profile_pic_id)
                            except Exception as e:
                                print(e,item['image_versions2']['candidates'])
                                ite.append('')
                            dtfechaD=datetime.strptime(fecha.split(' ')[0], "%Y-%m-%d")
                            fechaFinal=dtfechaD.strftime("%Y-%m-%d")
                            fechatest=fechatest
                            dtfechaTest=datetime.strptime(fechatest, "%Y-%m-%d")
                            fechaTest=dtfechaTest.strftime("%Y-%m-%d")
                            if(fechaFinal<=fechatest):
                                if(len(posts)>0):
                                    print('writing')
                                    writeCSV(posts,username)
                                return 0
                            else:
                            #ite.append(item[''])
                                posts.append(ite)
                        if temp["more_available"] == False:
                            next_max_id = False
                            writeCSV(posts,username)
                            return 0
                                
                        next_max_id = temp["next_max_id"]
                        g = API.getUserFeed(user_id,next_max_id)
                        temp = API.LastJson
                    except ValueError:
                        print(ValueError)
    except Exception as e:
        print(ValueError)



API = InstagramAPI(user,pwd)
API.login()
listaUsername=['itbearyoutube']
for x in listaUsername:
    getTimeline(str(x),'2019-05-01',API)
    time.sleep(4)