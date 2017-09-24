from __future__ import print_function

import numpy as np
from skimage.measure import compare_ssim
import argparse
import imutils
import glob
import cv2


def searchImageByMatchTemplate(template, target, threshold):

	global MAX_TAGET_IMAGE_WIDTH

	(templateH, templateW) = template.shape[:2]

	(tH, tW) = target.shape[:2]
	gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
	bFound = False
	found = (threshold, (0,0), 0)

	edged = cv2.Canny(target, 50, 200)
	result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
	(_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

	r = 1
	# if we have found a new maximum correlation value, then ipdate
	# the bookkeeping variable
	if maxVal > found[0]:
		#print('found: maxval = ', maxVal, 'r=', r)
		bFound = True
		found = (maxVal, maxLoc, r)

	if bFound == False:
		return (bFound, None, 0, (0,0), (0,0))

	(maxVal, maxLoc, r) = found
	(startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
	(endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

	crop_W = int(templateW*r)
	crop_H = int(templateH*r)
	crop_img = target[startY:startY+crop_H, startX:startX+crop_W]
	#weight = float(maxVal - threshold)/float(perfectMatch)

	return (bFound, crop_img, maxVal, (startX, startY), (startX+crop_W, startY+crop_H))
