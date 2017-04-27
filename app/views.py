from app import app, grabber, merge, segment
from flask import render_template, request, url_for, jsonify
import cv2
import numpy as np
import os, re

def rm(dir, pattern):
    for f in os.listdir(dir):
        if re.search(pattern, f):
            os.remove(os.path.join(dir, f))

@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html')


@app.route('/grabber/', methods=['POST'])
def doGrabber():
    # clean up folders
    rm('app/static/img', 'dg*')
    rm('app/ma_prediction_400','dg*')

    data = request.form
    lat = data['lat']
    lon = data['lon']
    zoom = data['zoom']

    with open('app/static/secrets.txt') as f: token = f.read()

    # get the location from digital globe
    g = grabber.Grabber('app/static/img', token,'png')
    time = g.grab(lat, lon, zoom, '832x469')

    # # 'smart' means that the image went through the neural net prediction script
    # smart_contours = segment.predict(time,'app/ma_prediction_400/dg%s.png'%(time), 'app/static/img/nn_dg'+time+'.png')
    # smart_areas = segment.get_areas(smart_contours.values())
    #
    # # 'dumb' meanas that the segmentation was on the original image
    # dumb_contours = segment.dumb_contours('app/static/img/dg'+time+'.png','app/static/img/dumy_dg'+time+'.png')
    # dumb_areas = segment.get_areas(dumb_contours.values())
    #
    # # uses 'smart' locations to pick out contours in the 'dumb' image
    # buildings = merge.intersect(smart_contours, dumb_contours)
    # merge.mkimage('app/static/img/dg'+time+'.png','app/static/img/merge_dg'+time+'.png', buildings)
    # areas = segment.get_areas(buildings.values())
    #
    # url_nn = url_for('static', filename='img/nn_base_dg'+time+'.png')
    # url_smart = url_for('static', filename='img/nn_dg'+time+'.png')
    # url_dumb = url_for('static', filename='img/dumy_dg'+time+'.png')
    # url_merge = url_for('static', filename='img/merge_dg'+time+'.png')

    # for cameron
    dumb_contours = segment.dumb_contours('app/static/img/dg'+time+'.png','app/static/img/dumy_dg'+time+'.png')
    dumb_areas = segment.get_areas(dumb_contours.values())

    drone_contours = segment.dumb_contours('app/static/img/stills/small/small_hyer.png', 'app/static/img/cont_hyer.png')
    drone_areas = segment.get_areas(drone_contours.values())


    url_dumb = url_for('static', filename='img/dumy_dg'+time+'.png')
    url_drone = url_for('static', filename='img/cont_hyer.png')

    return jsonify(url_drone=url_drone, url_dumb=url_dumb,
                   drone_areas=drone_areas, dumb_areas=dumb_areas,
                   )
