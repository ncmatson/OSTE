import numpy as np
import cv2
import random
import os

def dumb_contours(fin,fout):
    # us open_cv to get contours and their areas
    img = cv2.imread(fin)

    # crop to size of neural net output
    img = img[27:484,27:484]
    cv2.imwrite(fin,img)
    features = segmentation(fin,fout)
    return features #returns contours

def predict(time, fin, fout):
    # run prediction script
    val = os.system('./app/prediction.sh')

    features = segmentation(fin,fout)

    os.system('mv app/ma_prediction_400/dg%s.png app/static/img/nn_base_dg%s.png'%(time,time))
    return features #returns contours

def segmentation(fin, fout):
	img = cv2.imread(fin)
	Bchan,Gchan,Rchan = cv2.split(img)
	#Gchan = cv2.cvtColor(Gchan, cv2.COLOR_BGR2GRAY)
	# 0.6*255 60% confidence of building
	_,binimg = cv2.threshold(Gchan,153,255,cv2.THRESH_BINARY)
	binAdaptimg = cv2.adaptiveThreshold(Gchan,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,51,-2)


	#try findContours
	im2, contours, hierarchy = cv2.findContours(binimg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	out2 = np.zeros(img.shape,dtype=np.uint8)
	#out2[binimg == 255] = [0,0,255]
	#cv2.drawContours(out2,contours, -1, (0,255,255), 3)

	# find the center and area of each object
	# a feature is defined by its center (cx, cy) and its area
	features = {}
	area = np.zeros(len(contours))
	for i, c in enumerate(contours):
		r = random.randint(20,200)
		g = random.randint(20,200)
		b = random.randint(20,200)
		m = cv2.moments(c)
		if (m['m10'] > 0):
			# center location of each contour
			cx = int(m['m10']/m['m00'])
			cy = int(m['m01']/m['m00'])

			#mark each contour with a circle and a numeric label

			# add the location:area pair to list of features
			area = cv2.contourArea(c)
			if area > 20:
				features[(cx,cy)] = c
				cv2.drawContours(out2,c,-1,(0,255,255),2)
				cv2.fillPoly(out2, pts=[c], color=[r, g, b])
				cv2.circle(out2, (cx,cy), 5, [255,255, 255])
				cv2.putText(out2, str(i), (cx,cy), cv2.FONT_HERSHEY_PLAIN, 1, [255-b, 255-g, 255-r],1,8)
			# area[i] = cv2.contourArea(c)

	cv2.imwrite(fout,out2)

	return features

def get_areas(contours):
	areas = []
	for c in contours:
		areas.append(cv2.contourArea(c))
	return areas
