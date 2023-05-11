import requests
import network
url_users='https://pastebin.com/raw/BDCw0mWn'
url_ntfy='https://ntfy.sh/FabLabGuest'
def myusers():
  users=[]
  try:
    res = requests.get(url_users)
    for user in (res.text).split('\n'):
      user=user.replace('\r','')
      user=user.split(':')[1]
      users.append(user)
  except:
    pass
  print(users)
  res = requests.post(url_ntfy, data = users)
  return users
