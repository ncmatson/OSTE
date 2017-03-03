from app import app, grabber
from flask import render_template, request, url_for
import cv2
import numpy as np
from matplotlib import pyplot as plt
import os, re

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

@app.route('/grabber/', methods=['POST'])
def doGrabber():
    rm('app/static/img', 'dg*')
    data = request.form
    lat = data['lat']
    lon = data['lon']
    zoom = data['zoom']

    with open('app/static/secrets.txt') as f:
        token = f.read()

    g = grabber.Grabber('app/static/img', token)
    time = g.grab(lat, lon, zoom)
    edgeit('app/static/img/dg'+time+'.jpg')

    url = url_for('static', filename='img/dg'+time+'.jpg')
    return url
