import numpy as np
import cv2
import random

img = cv2.imread('dg1490743858.59531.png')
Bchan,Gchan,Rchan = cv2.split(img)
#Gchan = cv2.cvtColor(Gchan, cv2.COLOR_BGR2GRAY)
# 0.6*255 60% confidence of building
_,binimg = cv2.threshold(Gchan,153,255,cv2.THRESH_BINARY)
binAdaptimg = cv2.adaptiveThreshold(Gchan,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,51,-2)

cv2.imwrite('greenthresh.png',binimg)
cv2.imwrite('greengausthresh.png',binAdaptimg)

#noise removal
kernel = np.ones((5,5),np.uint8)
opening = cv2.morphologyEx(binimg,cv2.MORPH_OPEN,kernel,iterations=2)

#Finding background
sure_bg = cv2.dilate(opening,kernel,iterations=3)

#Finding foreground
#fast distance transform L2 size 3
#binDist = cv2.distanceTransform(opening,cv2.DIST_L2,5);
binDist = opening
_,sure_fg = cv2.threshold(binDist,0.7*binDist.max(),255,0);

#unknown area
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)

#label markers
_,markers = cv2.connectedComponents(sure_fg)

#markers define background (which are 0 value)
#we want unknown to be the only zero value, so we set bg=1
markers = markers+1

markers[unknown==255] = 0

markers = cv2.watershed(img,markers)

out = np.zeros(img.shape,dtype=np.uint8)
out[binimg == 255] = [0,0,255]
out[markers==-1] = [255,0,0]
cv2.imwrite('greendisttransform.png',out)

#try findContours
im2, contours, hierarchy = cv2.findContours(binimg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
print(len(contours))
out2 = np.zeros(img.shape,dtype=np.uint8)
out2[binimg == 255] = [0,0,255]
cv2.drawContours(out2,contours, -1, (0,255,255), 3)
cv2.imwrite('contours.png',out2)

# find the moments of each object
# M = np.zeros(len(contours))
for c in contours:
    r = random.randint(20,200)
    g = random.randint(20,200)
    b = random.randint(20,200)

    cv2.fillPoly(out2, pts=[c], color=[r, g, b])
    m = cv2.moments(c)
    if (m['m10'] > 0):
        cx = int(m['m10']/m['m00'])
        cy = int(m['m01']/m['m00'])
        cv2.circle(out2, (cx,cy), 5, [255,255, 255])

cv2.imwrite('contours.png', out2)
