from InstagramAPI import InstagramAPI
import time
from datetime import datetime
import random
from random import randint
def getFollower(username,pwd,handle):
    API = InstagramAPI(username,pwd)
    API.login()
    API.searchUsername(handle)
    user_id=API.LastJson['user']['pk']
    #followersLim  =367# 1 dia 2 000 000 user
    followers = []
    next_max_id = ''

    g = API.getUserFollowers(user_id,next_max_id)
    temp = API.LastJson
    taman=0
    print(temp,'-')
    while 1:
        try:
            while g==False:
                print("wait")
                n = randint(50,90)
                time.sleep(3*n)
                g = API.getUserFollowers(user_id,next_max_id)
                temp = API.LastJson
                print(temp,'-')
            for item in temp["users"]:
                try:
                    followers.append(str(item['pk']))
                except Exception as e:
                    print(e)
                    pass
            taman=taman+len(temp["users"])
            # if(taman>33000):
            #     print('llegue')
            #     thefile = open('C:/Users/jordy/Desktop/backup/ProyectoMavenRoad/instagram/' + handle+'.txt', 'w')
            #     thefile.write("\n".join(map(lambda x: str(x), followers)))
            #     thefile.close()
            #     break
            if(temp["big_list"] == False):
                break
            next_max_id = temp["next_max_id"]
            print(next_max_id)
            print(taman)

            g = API.getUserFollowers(user_id,next_max_id)
            temp = API.LastJson
        except Exception as e:
            print(e)
            print('end game')
    thefile = open('C:/Users/jordy/Desktop/backup/ProyectoMavenRoad/instagram/' + handle+'.txt', 'w')
    thefile.write("\n".join(map(lambda x: str(x), followers)))
    thefile.close() 
username='joshuabarr5'
pwd='jbarr123'
getFollower(username,pwd,'musiciansfriend')
getFollower(username,pwd,'zzoundsmusic')
getFollower(username,pwd,'monstersessions')
getFollower(username,pwd,'damemonster')
getFollower(username,pwd,'nyusteinhardtmusic')
getFollower(username,pwd,'nyusteinhardtvp')
getFollower(username,pwd,'nyumusictech')
getFollower(username,pwd,'nyumusicbiz')
getFollower(username,pwd,'nyumusiced')
getFollower(username,pwd,'nycmusicians')
getFollower(username,pwd,'vassarcollege')
getFollower(username,pwd,'colgateuniversity')
getFollower(username,pwd,'nyusteinhardt')
getFollower(username,pwd,'inflightmusicgroup')
getFollower(username,pwd,'hunnypotlive')
getFollower(username,pwd,'revival.la')
getFollower(username,pwd,'diamondminestudios')
getFollower(username,pwd,'endure_studios')
getFollower(username,pwd,'skylinestudios')
getFollower(username,pwd,'solidstatelogic')
getFollower(username,pwd,'RRFConnection')








