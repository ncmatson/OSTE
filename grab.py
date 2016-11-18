import urllib

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

picture_id = 'nal0g75k'
#url1 = 'https://api.mapbox.com/v4/digitalglobe.nal0g75k/86.925,27.9878,10/450x450.png256?access_token=pk.eyJ1IjoiZGlnaXRhbGdsb2JlIiwiYSI6ImNpdHRkOWk0ZDAwMTUzMG4yM2g5Nmhtb2wifQ.O-5kuQ4vKzy0lcuqMAbBMA'
url = 'https://api.mapbox.com/v4/digitalglobe.'+picture_id+'/'+loc+'/'+size+'.'+form+'?access_token='+access_token
#print url1
#print url2
#print (url1==url2)
urllib.urlretrieve(url, "local.png")
