import numpy as np
import cv2
import random

#input dictionary of {centroids,contours}
#return dictionary of centroids in dumb that can fit in smart
def intersect(smart,dumb):

    if len(smart) > len(dumb):
        return smart

    sdic = {}
    for sloc in smart:
        mindist = 10**8;#dummy distance
        for dloc in dumb:
            dist = (sloc[0]-dloc[0])**2 + (sloc[1]-dloc[1])**2
            if dist < mindist:
                mindist = dist
                loc = dloc
        sdic[loc] = dumb[loc]
        #sdic contains shapes of "correctly" identified buildings
    return sdic


def mkimage(fin,fout,thecontours,base=1):
    img = cv2.imread(fin)
    out = np.zeros(img.shape,dtype=np.uint8)
    if(base == 1):
        out = img
    i=0
    for loc in thecontours.keys():
        c = thecontours[loc]
        r = random.randint(20,200)
        g = random.randint(20,200)
        b = random.randint(20,200)
        cv2.drawContours(out,[c],-1,(0,255,255),2)
        cv2.fillPoly(out, pts=[c], color=[r, g, b])
        cv2.circle(out, loc, 5, [255,255, 255])
        cv2.putText(out, str(i), loc, cv2.FONT_HERSHEY_PLAIN, 1, [255-b, 255-g, 255-r],1,8)
        i=i+1

    cv2.imwrite(fout,out)
