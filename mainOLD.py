import mfrc522
from os import uname
import network, machine, time
import urequests as requests


led = machine.Pin(2, machine.Pin.OUT)

for k in range(3):
    led.on()
    time.sleep(1)
    led.off()
    time.sleep(1)

print('On the way')


url_users='https://pastebin.com/raw/M9eGvFxS'
url_ntfy='https://ntfy.sh/FabLabGuest'
#url_ntfy_new='http://ntfy.sh/<SujetNouvellesCartes>'

#Nbre de led Neopixels
#nbr_leds=16
#OnBoard led pour verifier si l'esp se connecte
led = machine.Pin(2, machine.Pin.OUT)
#NeoPixel sur pin D6:
#ring = neopixel.NeoPixel(machine.Pin(12), nbr_leds)
#couleurs=[(255, 102, 0), (255, 0, 102),(153, 51, 255),(0, 0, 255),(63, 255, 63)]
#Petite animation de lancement
#for c in coulours():
#for k in range(16):
          #ring[k] =[(255, 102, 0), (255, 0, 102),(153, 51, 255),(0, 0, 255),(63, 255, 63)]
          #ring.write()
          #time.sleep(0.1)

#sta_if=network.WLAN(network.STA_IF)
#if not sta_if.isconnected():
#    sta_if.active(True)
#    sta_if.connect('FabLab','FabLab66')
#    while not sta_if.isconnected():
#      pass
print(sta_if.ifconfig())
users={}
try:
  res = requests.get(url_users)
  for user in (res.text).split('\n'):
    users[user.split(':')[0]]=user.replace('\r','').split(':')[1]
  print(users)
except:
  c=(128,63,0)
  #for k in range(nbr_leds):
   # ring[k] = c
    #ring.write()
    #time.sleep(0.1)
  pass
rdr = mfrc522.MFRC522(0, 2, 4, 5, 14)
rdr.antenna_on()
state=0
user_in=''
try:
    
 while True:
    print("we are in loop")
    (stat, tag_type) = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
      (stat, raw_uid) = rdr.anticoll()
      if stat == rdr.OK:
        u="0x%02x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3], raw_uid[4])
        try:

          #Si l’utilisateur existe il est pris en compte
          utilisateur=users[u]
        except:

          #Si l’utilisateur n’existe pas il est appelé “Quelqu’un”
          utilisateur="Quelqu'un"
          post_data=(u).encode('utf-8')
          #Comme c’est un nouvel utilisateur son numéro de carte est envoyé sur le salon dédié pour être envoyé sur 
          res = requests.post(url_ntfy_new, data = post_data)
        if state==1 and utilisateur==user_in:
          state=0
          user_in=''
          post_data=("🔴 "+utilisateur+" vient de fermer le FabLab").encode('utf-8')
          couleur=(255,0,0) #Rouge
        elif state==1 and utilisateur!=user_in:
          state=1
          user_in=utilisateur
          post_data=("🟢 "+utilisateur+" vient de prendre la responsabilité du FabLab").encode('utf-8')

          #Petite anim pour montrer que le changement de responsabilité a été pris en compte
          couleur=(0,255,0) #Vert
          for i in range(2):
            for k in range(nbr_leds-1):
              ring[k] = couleur
              if couleur==(0,255,0):
                couleur=(255,0,0)
              else:
                couleur=(0,255,0)
              ring.write()
              time.sleep(0.1)
          couleur=(0,255,0) #Vert
        else:
          state=1
          user_in=utilisateur
          couleur=(0,255,0) #Vert
          post_data=("🟢 "+utilisateur+" vient d'ouvrir le FabLab").encode('utf-8')
        res = requests.post(url_ntfy, data = post_data)
        for i in range(2):
          #for k in range(nbr_leds):
            #ring[k] = couleur
            #ring.write()
            #time.sleep(0.1)
          pass
except KeyboardInterrupt:
  pass
  print("Bye")
