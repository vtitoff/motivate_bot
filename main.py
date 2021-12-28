import requests as r
import json

token = ''
url = f'https://api.telegram.org/bot{token}/getMe'

# https://api.telegram.org/bot<token>/method
print(r.get(url).json())
