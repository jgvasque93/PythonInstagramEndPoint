#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
import requests
import json
import  re
#'https://www.instagram.com/web/search/topsearch/?query={query}'
def getEngagement(code):
	info=[]
	endPoint='https://www.instagram.com/p/code/?__a=1'
	res=requests.get(endPoint.replace('code',code))
	try:
		_comment_count=res.json()['graphql']['shortcode_media']['edge_media_to_comment']['count']
		_favorite_count=res.json()['graphql']['shortcode_media']['edge_media_preview_like']['count']
		text=res.json()['graphql']['shortcode_media']['edge_media_to_caption']['edges'][0]['node']['text']
		info.append(code)
		info.append(text)
		info.append(_comment_count)
		info.append(_favorite_count) 
		return info
	except Exception as e:
		print(e)
		return None

print(getEngagement('BqP8wKlhV9z'))
print(getEngagement('BsiTOvghTrg'))
print(getEngagement('Br0dCx_hH4X'))