import requests

def get_media_id(url):
    req = requests.get('https://api.instagram.com/oembed/?url={}'.format(url))
    media_id = req.json()['media_id']
    return media_id

print(get_media_id('https://www.instagram.com/p/BrxvsaQh2XT/'))
print(get_media_id('https://www.instagram.com/p/BusTJN8lVJm/'))
print(get_media_id('https://www.instagram.com/p/BuTG_mzlrfY/'))