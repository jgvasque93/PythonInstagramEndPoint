from InstagramAPI import InstagramAPI
import time
from datetime import datetime
import random
from random import randint
import getFollower
import getFollowing 

def unfollow(username,pwd,listFollower,LitsFollowing):
	API = InstagramAPI(username,pwd)
	API.login()
	s1 = set(listFollower)
	s2 = set(LitsFollowing)
	s3=s2-s1
	lista=list(s3)

	print('Numero de followers ',len(s1))
	print('Numero de Followigs',len(s2))

	print('Total de unfollows',len(lista))
	for x in lista:
		print(x)
		g=API.unfollow(x)
		while g==False:
			print("wait")
			n = randint(50,90)
			time.sleep(3*n)
			g = API.unfollow(x)
		time.sleep(5)
 

username = 'user'
pwd = 'password'
s1=getFollowing.getFollowing(username,pwd)
s2=getFollower.getFollower(username,pwd)
unfollow(username,pwd,s2,s1)