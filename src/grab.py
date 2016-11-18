import urllib
import time

access_token = 'pk.eyJ1IjoiZGlnaXRhbGdsb2JlIiwiYSI6ImNpdHRkOWk0ZDAwMTUzMG4yM2g5Nmhtb2wifQ.O-5kuQ4vKzy0lcuqMAbBMA'
lat = 38.8966
lon = -77.0365
z   = 16

loc = str(lon)+','+str(lat)+','+str(z)
loc

h = 450
w = 450

size = str(w)+'x'+str(h)
size

form = 'jpg90'

dest = '../img/'+str(int(time.time()))+'.jpg'

picture_id = 'digitalglobe.nako1fhg'
url = 'https://api.mapbox.com/v4/'+picture_id+'/'+loc+'/'+size+'.'+form+'?access_token='+access_token
urllib.urlretrieve(url, dest)
