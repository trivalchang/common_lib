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
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)	

	# reshape the image to be a list of pixels
	image = image.reshape((image.shape[0] * image.shape[1], 3))

	# cluster the pixel intensities
	clt = KMeans(n_clusters = clusterNo)
	clt.fit(image)

	numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
	(hist, _) = np.histogram(clt.labels_, bins = numLabels)

	# normalize the histogram, such that it sums to one
	hist = hist.astype("float")
	hist /= hist.sum()
	hist *= 100
	#bar = utils.plot_colors(hist, clt.cluster_centers_)

	colorList = []
	for (percent, color) in zip(hist, clt.cluster_centers_):
		# plot the relative percentage of each cluster
		colorList.append([int(percent), color.astype("uint8").tolist()])
	return colorList
