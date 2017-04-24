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

def get_contours(img):
    # us open_cv to get contours and their areas
    features = segment.segmentation(img,img)
    return features

def classify(time, img):
    #need to create copy of image to work with interpolation
    # i = cv2.imread(img)
    # input = cv2.resize(i,(0,0),i,fx=2,fy=2,interpolation=cv2.INTER_CUBIC)
    # print(input.shape[:2])
    # cv2.imwrite('app/static/img/interpdg%s.png'%(time),i)#create copy for testing interp

    # run prediction script
    val = os.system('./app/prediction.sh')

    features = segment.segmentation('app/ma_prediction_400/dg%s.png'%(time),img)
    # un_areas = segment.segmentation('app/ma_prediction_400/interpdg%s.png'%(time),'app/static/img/interpdg'+time+'.png')
    return features

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

    # dumb areas are from the image that didn't go through the prediciton
    dumb_areas = get_contours('app/static/img/dg'+time+'.png')

    # smart areas are in the image that went through the prediction
    # smart_areas = classify(time, 'app/static/img/dg'+time+'.png')



    url = url_for('static', filename='img/dg'+time+'.png')

    return jsonify(url=url,
                   areas=list(dumb_areas.values())
                   )
