import urllib
import time

access_token = 'pk.eyJ1IjoiZGlnaXRhbGdsb2JlIiwiYSI6ImNpdHRkOWk0ZDAwMTUzMG4yM2g5Nmhtb2wifQ.O-5kuQ4vKzy0lcuqMAbBMA'
lon = 86.925
lat = 27.9878
z   = 5

loc = str(lon)+','+str(lat)+','+str(z)
loc

h = 450
w = 450

size = str(w)+'x'+str(h)
size

form = 'png256'

dest = '../img/'+str(int(time.time()))+'.png'

picture_id = 'nal0g75k'
url = 'https://api.mapbox.com/v4/digitalglobe.'+picture_id+'/'+loc+'/'+size+'.'+form+'?access_token='+access_token
urllib.urlretrieve(url, dest)
