from app import app, grabber
from flask import render_template, request, url_for
import cv2
import numpy as np
from matplotlib import pyplot as plt
import os, re
import subprocess
import segment
#from config import MEDIA_FOLDER

@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html')

def rm(dir, pattern):
    for f in os.listdir(dir):
        if re.search(pattern, f):
            os.remove(os.path.join(dir, f))

def edgeit(img):
    i = cv2.imread(img)
    edges = cv2.Canny(i,100,200)
    cv2.imwrite(img, edges)

def segit(img):
    i = cv2.imread(img)
    gray = cv2.cvtColor(i,cv2.COLOR_BGR2GRAY)
    cv2.imwrite('app/static/img/gray.jpg', gray)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    cv2.imwrite(img, thresh)


def predict(time):
	#call(['echo $PWD'],shell=True)
	#call(['app/sample.sh'],shell=True)
    process = subprocess.call(['./app/prediction.sh'],shell=True)
    #process2 = subprocess.call(['cp','app/ma_prediction_400/dg%s.png'%(time),'app/static/css/images/dg%s.png'%(time)],shell=True)
    segment.segmentation('app/ma_prediction_400/dg%s.png'%(time),'app/static/img/dg%s.png'%(time))
    return process2.wait()

@app.route('/grabber/', methods=['POST'])
def doGrabber():
    rm('app/static/img', 'dg*')
    rm('app/ma_prediction_400','dg*')
    data = request.form
    lat = data['lat']
    lon = data['lon']
    zoom = data['zoom']

    with open('app/static/secrets.txt') as f:
        token = f.read()

    g = grabber.Grabber('app/static/img', token,'png')
    time = g.grab(lat, lon, zoom)
    # edgeit('app/static/img/dg'+time+'.jpg')
    # segit('app/static/img/dg'+time+'.jpg')
    delay = predict(time)
    segment.segmentation('app/ma_predication/dg%s.png'%(time),'app/static/img/dg%s.png'%(time))

    
    #url = url_for('.index',filename='ma_prediction_400/dg%s.png'%(time))
#url_for('ma_prediction_400', filename='/dg'+time+'.png')
    #return url
