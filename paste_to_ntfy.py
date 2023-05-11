import requests
import network
url_users='https://pastebin.com/raw/BDCw0mWn'
url_ntfy='https://ntfy.sh/FabLabGuest'
users={}
try:
  res = requests.get(url_users)
  for user in (res.text).split('\n'):
    users[user.split(':')[0]]=user.replace('\r','').split(':')[1]
  print(users)
except:
  pass

res = requests.post(url_ntfy, data = users)
