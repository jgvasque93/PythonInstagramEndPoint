from InstagramAPI import InstagramAPI
import time
from datetime import datetime
import random
from random import randint

def getFollowing(username,pwd,handle):
    API = InstagramAPI(username,pwd)
    API.login()
    API.searchUsername(handle)
    user_id=API.LastJson['user']['pk']
    #followersLim  =367# 1 dia 2 000 000 user
    followers = []
    next_max_id = ''

    g = API.getUserFollowings(user_id,next_max_id)
    temp = API.LastJson
    while 1:
        try:
            while g==False:
                print("wait")
                n = randint(50,90)
                time.sleep(3*n)
                g = API.getUserFollowings(user_id,next_max_id)
                temp = API.LastJson
            for item in temp["users"]:

                followers.append(item['pk'])
            if(temp["big_list"] == False):
                break
            next_max_id = temp["next_max_id"]
            print(next_max_id)
            g = API.getUserFollowings(user_id,next_max_id)
            temp = API.LastJson
        except Exception as e:
            print(e)
            print('end game')
    thefile = open('C:/Users/jordy/Desktop/backup/ProyectoMavenRoad/instagram/' + handle+'.txt', 'w')              
    thefile.write("\n".join(map(lambda x: str(x), followers)))
    thefile.close() 
username='User'
pwd='PASSWORD'
getFollowing(username,pwd,'matt_horwitz')