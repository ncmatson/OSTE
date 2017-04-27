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

    # use the drone image
    dumb_contours = segment.dumb_contours('app/static/img/stills/small/small_dallas.png', 'app/static/img/dumy_dallas2.png')
    dumb_areas = segment.get_areas(dumb_contours.values())

    areas = dumb_areas
    url_dumb = url_for('static', filename='img/dumy_dallas2.png')

    return jsonify(url_dumb=url_dumb, areas=areas)
