from numpy import *

#feature numbering is consistent with paper by Premebida et al. (LIDAR...)
#whenever a cluster is passed it is one of the entries in the clusters array,so a triplet containing first point's index, last point's index, number of points

class FeatureExtraction:
    def extractFeatures(self, cluster, polar, cartesian):
        featureVector = []
        featureVector.append(self.feature1(cluster, polar))
        featureVector.append(self.feature2(cluster))
        featureVector.append(self.feature3(cluster, cartesian))
        featureVector.append(self.feature4(cluster, cartesian))
        featureVector.append(self.feature6(cluster, cartesian))
        featureVector.append(self.feature14(cluster, cartesian))
        featureVector.append(self.feature15(cluster, cartesian))

        return featureVector

    def feature1(self, cluster, polar):
        index = cluster[0]
        min = polar[index][0]
        while (index <= cluster[1]):
            if (polar[index][0] < min):
                min = polar[index][0]
            index += 1
        return cluster[2] * min

    def feature2(self, cluster):
        return cluster[2]

    def feature3(self, cluster, cartesian):
        return sqrt(pow((cartesian[cluster[0]][0] - cartesian[cluster[1]][0]), 2) + pow((cartesian[cluster[0]][1] - cartesian[cluster[1]][1]), 2))

    def feature4(self, cluster, cartesian):
        centroid = (cartesian[cluster[1]][0] - cartesian[cluster[0]][0]) / 2
        sum = 0.0
        for index in range(cluster[0], cluster[1]):
            sum += abs(cartesian[index][0] - centroid)
        return sqrt(sum/cluster[2])

    def feature6(self, cluster, cartesian):
        tempArray = []
        for index in range(cluster[0], cluster[1]):
            tempArray.append(cartesian[index][0])
        med = median(tempArray)
        sum = 0
        for index in range(cluster[0], cluster[1]):
            sum += abs(cartesian[index][0] - med)
        return sum/cluster[2]

    def feature14(self, cluster, cartesian):
        sum = 0
        for index in range(cluster[0], cluster[1] - 1):
            sum += abs(cartesian[index][0] - cartesian[index + 1][0])
        return sum

    def feature15(self, cluster, cartesian):
        tempArray = []
        for index in range(cluster[0], cluster[1] - 1):
            tempArray.append(abs(cartesian[index][0] - cartesian[index + 1][0]))
        return std(tempArray)
