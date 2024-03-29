# USAGE
# python color_kmeans.py --image images/jp.png --clusters 3

# import the necessary packages
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import argparse
import utils
import cv2

def findDominantColor(image, clusterNo):
	e1 = cv2.getTickCount()
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)	
	e2 = cv2.getTickCount()
	# reshape the image to be a list of pixels
	image = image.reshape((image.shape[0] * image.shape[1], 3))
	e3 = cv2.getTickCount()
	# cluster the pixel intensities
	clt = KMeans(n_clusters = clusterNo)
	e4 = cv2.getTickCount()	
	clt.fit(image)
	e5 = cv2.getTickCount()
	numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
	(hist, _) = np.histogram(clt.labels_, bins = numLabels)

	# normalize the histogram, such that it sums to one
	hist = hist.astype("float")
	hist /= hist.sum()
	hist *= 100
	#bar = utils.plot_colors(hist, clt.cluster_centers_)
	e6 = cv2.getTickCount()

	colorList = []
	for (percent, color) in zip(hist, clt.cluster_centers_):
		# plot the relative percentage of each cluster
		colorList.append([int(percent), color.astype("uint8").tolist()])
	return sorted(colorList)
