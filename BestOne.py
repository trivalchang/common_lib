from __future__ import print_function

import numpy as np
from skimage.measure import compare_ssim
import argparse
import imutils
import glob
import cv2

WINDOW_GAP = 200

def showImage(title, image, x, y):
	cv2.imshow(title, image)
	cv2.moveWindow(title, x, y)

def compareDominantColor(dominant0, dominant1):
	index = 0
	diff = 0
	dominant0 = sorted(dominant0)
	dominant1 = sorted(dominant1)
	color0 = []
	color1 = []
	print('dor0 ', dominant0)
	print('dor1 ', dominant1)	
	for index in range(0, len(dominant0)):
		#color0 = dominant0[index][0] * (dominant0[index][1][0] + dominant0[index][1][1] + dominant0[index][1][2])
		#color1 = dominant1[index][0] * (dominant1[index][1][0] + dominant1[index][1][1] + dominant1[index][1][2])
		if (dominant0[index][1][0] != 0):
			color0.append(float(dominant0[index][1][1]-dominant0[index][1][0])/dominant0[index][1][0])
		else:
			color0.append(1)
		if (dominant0[index][1][1] != 0): 
			color0.append(float(dominant0[index][1][2]-dominant0[index][1][1])/dominant0[index][1][1])
		else:
			color0.append(1)
		if (dominant0[index][1][0] != 0):
			color0.append(float(dominant0[index][1][2]-dominant0[index][1][0])/dominant0[index][1][0])
		else:
			color0.append(1)

		if (dominant1[index][1][0] != 0):
			color1.append(float(dominant1[index][1][1]-dominant1[index][1][0])/dominant1[index][1][0])
		else:
			color1.append(1)
		if (dominant1[index][1][1] != 0):
			color1.append(float(dominant1[index][1][2]-dominant1[index][1][1])/dominant1[index][1][1])
		else:
			color1.append(1)
		if (dominant1[index][1][0] != 0):
			color1.append(float(dominant1[index][1][2]-dominant1[index][1][0])/dominant1[index][1][0])
		else:
			color1.append(1)

		break

	diff = abs(color0[0]-color1[0])+abs(color0[1]-color1[1])+abs(color0[2]-color1[2])

	print('color0 = ', color0)
	print('color1 = ', color1)
	print('diff ', diff)
	return diff

def colorMatchSsim(template, target, channel, virtualized, x, y):
	global WINDOW_GAP

	(tH, tW) = target.shape[:2]
	if (virtualized == True):
		showImage('target'+str(x)+str(y), target, x, y)
		x = x + WINDOW_GAP

	targetSingleColor = cv2.split(target)[channel]
	templateColor = cv2.resize(template, (tW, tH))
	templateColor = cv2.split(templateColor)[channel]
	(score, diff) = compare_ssim(templateColor, targetSingleColor, full=True, multichannel=False)
	#print('colorMatchSsim ', template[0], 'score =', score)

	if (virtualized == True):
		showImage(template + ' ' + str(score), template, x, y)
		x = x + WINDOW_GAP

		showImage('target color', target, x, y)
		x = x + WINDOW_GAP

		showImage('temp color', templateColor, x, y)
		x = x + WINDOW_GAP
		
		showImage('diff' + str(score), diff, x, y)
		x = x + WINDOW_GAP
	
	return score

def grayMatchSsim(templateList, target, virtualized, x, y):
	global WINDOW_GAP

	(tH, tW) = target.shape[:2]
	if (virtualized == True):
		showImage('target'+str(x)+str(y), target, x, y)
		x = x + WINDOW_GAP

	target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
	scoreList = []
	diffList = []
	templateTransformList = []
	for template in templateList:
		templateImg = cv2.resize(template[1], (tW, tH))
		templateImg = cv2.cvtColor(templateImg, cv2.COLOR_BGR2GRAY)
		templateTransformList.append(templateImg)
		(score, diff) = compare_ssim(templateImg, target, full=True, multichannel=True)
		scoreList.append(score)
		diffList.append(diff)
		print('grayMatchSssim ', template[0], 'score =', score)

	if (virtualized == True):
		for idx in range(0, len(templateList)):
			showImage(templateList[idx][0] + ' ' + str(scoreList[idx]), templateList[idx][1], x, y)
			x = x + WINDOW_GAP

		showImage('target gray'+str(x)+str(y), target, x, y)
		x = x + WINDOW_GAP

		for idx in range(0, len(templateTransformList)):
			showImage('temp gray'+str(x)+str(y), templateTransformList[idx], x, y)
			x = x + WINDOW_GAP

		for idx in range(0, len(templateList)):
			showImage('diff' + str(idx) + ' ' + str(scoreList[idx]), diffList[idx], x, y)
			x = x + WINDOW_GAP
	whichOne = 0
	maxVal = scoreList[0]
	for idx in range(0, len(scoreList)-1):
		if (scoreList[idx]>maxVal):
			whichOne = idx
			maxVal = scoreList[idx]
	return whichOne

def hsvMatchSsim(template, target, channel, threshold, virtualized, x, y):
	global WINDOW_GAP

	(tH, tW) = target.shape[:2]

	if (virtualized == True):
		showImage('target'+str(x)+str(y), target, x, y)
		x = x + WINDOW_GAP
	target = cv2.cvtColor(target, cv2.COLOR_BGR2HSV)
	target = cv2.split(target)[channel]	

	#_, target = cv2.threshold(target, threshold, 0, cv2.THRESH_TOZERO)
	_, target = cv2.threshold(target, threshold, 255, cv2.THRESH_BINARY)
	if (virtualized == True):
		showImage('threshold'+str(threshold)+' '+str(x)+str(y), target, x, y)
		x = x + WINDOW_GAP

	scoreList = 0
	templateHSV = cv2.resize(template, (tW, tH))
	templateHSV = cv2.cvtColor(templateHSV, cv2.COLOR_BGR2HSV)
	templateHSV = cv2.split(templateHSV)[channel]
	#_, templateHSV = cv2.threshold(templateHSV, threshold, 255, cv2.THRESH_BINARY)
	(score, diff) = compare_ssim(templateHSV, target, full=True, multichannel=False)
	#print('hsvMatchSsim channel', template, 'channe= ', channel, 'score =', score)

	if (virtualized == True):
		showImage('template ' + str(score), template, x, y)
		x = x + WINDOW_GAP

		showImage('target HSV'+str(channel), target, x, y)
		x = x + WINDOW_GAP

		showImage('temp HSV '+str(channel), templateHSV, x, y)
		x = x + WINDOW_GAP
		
		showImage('diff' + str(channel), diff, x, y)
		x = x + WINDOW_GAP
	
	return score

