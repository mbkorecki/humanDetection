import skimage
from skimage import exposure
from skimage import feature
from skimage import data
from skimage import color
from matplotlib import pyplot as plt
from skimage.feature import hog
from sklearn import svm
from sklearn.metrics import classification_report, accuracy_score
import cv2
import numpy as np
import time
import json
from glob import glob
import os
import random
from PIL import Image

class HOG:
	def extractFeatures(self, image, ROI):
		img = image
		img = np.array(img).astype('uint8')
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		aspectRatio = 96/160
		newWidth = 6
		newHeight = 10
		while ((newWidth + 6 <= ROI[0] or newHeight + 10 <= ROI[1]) and not(newWidth + 6 >= 640 or newHeight + 10 + ROI[3] >= 480)):
			newWidth = newWidth + 6
			newHeight = newHeight + 10
		if ROI[2] - newWidth / 2 > 0:
			img = img[ROI[3]:ROI[3] + newHeight, ROI[2] - (newWidth / 2):ROI[2] + (newWidth / 2)]
			img = cv2.resize(img, (96, 160), interpolation = cv2.INTER_AREA)
			H = feature.hog(img, orientations = 9, pixels_per_cell = (8, 8),
				        cells_per_block = (2, 2), transform_sqrt = True, block_norm = "L2-Hys",
				        visualise = False)
			H = H.reshape(1, -1)
			return H
		else:
			return [0, 0, 0, 0]
