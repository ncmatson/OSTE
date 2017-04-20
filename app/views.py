from app import app, grabber
from flask import render_template, request, url_for, jsonify
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
    # i = cv2.imread(img)
    # edges = cv2.Canny(i,100,200)
    # cv2.imwrite(img, edges)
    areas = segment.segmentation(img,img)
    return areas.tolist()

def segit(img):
    i = cv2.imread(img)
    gray = cv2.cvtColor(i,cv2.COLOR_BGR2GRAY)
    cv2.imwrite('app/static/img/gray.jpg', gray)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    cv2.imwrite(img, thresh)


def predict(time, img):
	#call(['echo $PWD'],shell=True)
	#call(['app/sample.sh'],shell=True)
    #process = subprocess.call(['./app/prediction.sh'],shell=True)
    #need to create copy of image to work with interpolation
    #cv2.imwrite('wow'+img,)
    input = cv2.imread(img)
    input = cv2.resize(input,(0,0),input,fx=2,fy=2,interpolation=cv2.INTER_CUBIC)
    print(input.shape[:2])
    cv2.imwrite('app/static/img/interpdg%s.png'%(time),input)#create copy for testing interp
    val = os.system('./app/prediction.sh')
    print(val)
    print('testtext')
    #process2 = subprocess.call(['cp','app/ma_prediction_400/dg%s.png'%(time),'app/static/css/images/dg%s.png'%(time)],shell=True)
    areas = segment.segmentation('app/ma_prediction_400/dg%s.png'%(time),img)
    areas2 = segment.segmentation('app/ma_prediction_400/interpdg%s.png'%(time),'app/static/img/interpdg'+time+'.png')
    return areas.tolist()

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
    #areas = edgeit('app/static/img/dg'+time+'.png')
    areas = predict(time, 'app/static/img/dg'+time+'.png')

    url = url_for('static', filename='img/dg'+time+'.png')



    return jsonify(url=url,
                   areas=areas)
