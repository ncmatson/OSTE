from app import app, grabber, merge, segment
from flask import render_template, request, url_for, jsonify
import cv2
import numpy as np
from matplotlib import pyplot as plt
import os, re
import subprocess
#from config import MEDIA_FOLDER

@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html')

def rm(dir, pattern):
    for f in os.listdir(dir):
        if re.search(pattern, f):
            os.remove(os.path.join(dir, f))

def dumb_contours(fin,fout):
    # us open_cv to get contours and their areas
    img = cv2.imread(fin)

    # crop to size of neural net output
    img = img[27:484,27:484]
    cv2.imwrite(fin,img)
    features = segment.segmentation(fin,fout)
    return features #returns contours

def predict(time, fin, fout):
    # run prediction script
    val = os.system('./app/prediction.sh')

    features = segment.segmentation(fin,fout)

    os.system('mv app/ma_prediction_400/dg%s.png app/static/img/nn_base_dg%s.png'%(time,time))
    return features #returns contours


@app.route('/grabber/', methods=['POST'])
def doGrabber():
    rm('app/static/img', 'dg*')
    rm('app/ma_prediction_400','dg*')
    data = request.form
    lat = data['lat']
    lon = data['lon']
    zoom = data['zoom']

    with open('app/static/secrets.txt') as f: token = f.read()

    g = grabber.Grabber('app/static/img', token,'png')
    time = g.grab(lat, lon, zoom)

    # smart areas are in the image that went through the prediction
    smart_contours = predict(time,'app/ma_prediction_400/dg%s.png'%(time), 'app/static/img/nn_dg'+time+'.png')
    smart_areas = segment.get_areas(smart_contours.values())

    # dumb areas are from the image that didn't go through the prediciton
    dumb_contours = dumb_contours('app/static/img/dg'+time+'.png','app/static/img/dumy_dg'+time+'.png')
    dumb_areas = segment.get_areas(dumb_contours.values())

    buildings = merge.intersect(smart_contours, dumb_contours)
    merge.mkimage('app/static/img/dg'+time+'.png','app/static/img/merge_dg'+time+'.png', buildings)
    areas = segment.get_areas(buildings.values())

    # url_nn = '/ma_prediction_400/nn_dg%s.png'%(time)
    url_nn = url_for('static', filename='img/nn_base_dg'+time+'.png')
    url_smart = url_for('static', filename='img/nn_dg'+time+'.png')
    url_dumb = url_for('static', filename='img/dumy_dg'+time+'.png')
    url_merge = url_for('static', filename='img/merge_dg'+time+'.png')

    # return jsonify(url=url,
    #                areas=list(dumb_areas.values())
    #                )
    return jsonify(url=url_nn, url_smart=url_smart, url_dumb=url_dumb, url_merge=url_merge,
                   areas=areas
                   )
