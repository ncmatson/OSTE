import urllib.request
import time

class Grabber():
    """grabber sets up the api to grb images from the Digital globe
    site"""
    def __init__(self, dest, token, form='jpg'):
        self.time = str(time.time())
        self.token = token
        self.map_id = 'digitalglobe.nal0g75k'

        # location to store the grabbed images
        self.dest = dest

        # type of images to grab either (jpg or png)
        if form == 'png':
            self.ext = '.png'
            self.form = 'png256'
        else:
            self.ext = '.jpg'
            self.form = 'jpg90'

    def grab(self, lat, lon, zoom, size='512x512'):
        name = 'dg'+self.time
        loc = str(lon) + ',' + str(lat) + ',' + str(zoom)

        path = self.dest + '/' + name + self.ext
        url = 'https://api.mapbox.com/v4/'+self.map_id+'/'+loc+'/'+size+'.'+self.form+'?access_token='+self.token
        urllib.request.urlretrieve(url, path)

        return self.time
