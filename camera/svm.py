import numpy as np
import json
from matplotlib import pyplot as plt
from skimage import color
from skimage.feature import hog
from sklearn import svm
from sklearn.metrics import classification_report,accuracy_score
from subprocess import check_output
import cPickle

class SVM:
    def __init__(self):
        with open('svm_model', 'rb') as fid:
            self.model = cPickle.load(fid)

    def classify(self, hog):
        prediction = self.model.predict(hog)
        print "SVM prediction: ", prediction
