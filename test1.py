#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
import requests
import json
import  re
#'https://www.instagram.com/web/search/topsearch/?query={query}'
def getEndpoint(idUser):
	info=[]
	idUser=idUser.replace('\"','')
	endPoint='https://i.instagram.com/api/v1/users/idUser/info/'
	res=requests.get(endPoint.replace('idUser',idUser))
	try:
		full_name=json.dumps(res.json()['user']['full_name'])
		try:
			fullName=re.sub('[^a-zA-Z \n]', ' ',full_name).lower().replace(',', ' ').replace('\n', ' ').replace('\r', ' ')
			fullName=" ".join(fullName.split())
			info.append(fullName)
		except Exception as e:
			print(e)
			info.append('')
		followersCount=json.dumps(res.json()['user']['follower_count'])
		followingCount=json.dumps(res.json()['user']['following_count'])
		username=json.dumps(res.json()['user']['username']).replace('\"','')
		info.append(username)
		info.append(followersCount)
		info.append(followingCount) 
		return info
	except Exception as e:
		print(e)
		return None

print(getEndpoint('7227258103'))