import requests as r
import json

url = 'https://api.telegram.org'
token = ''
# https://api.telegram.org/bot<token>/method
print(r.get(url, token=token).json())