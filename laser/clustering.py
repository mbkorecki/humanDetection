from numpy import *

class Clustering:
    def generateClusters(self, polar):
        clusters = []
        clusters.append([0, 0, 0])
        index = 0
        n_points = 0

        for idx in range(0, len(polar) - 1):
            n_points += 1
            if (self.euclidianDistance(polar[idx], polar[idx + 1]) > 0.1):
                clusters[index][1] = idx
                clusters[index][2] = n_points
                clusters.append([idx + 1, 0, 0])
                n_points = 0
                index += 1
                del clusters[len(clusters) - 1]
        return clusters

    def euclidianDistance(self, coordinate1, coordinate2):
        return sqrt(square(coordinate1[0]) + square(coordinate2[0]) - 2 * coordinate1[0] * coordinate2[0] * cos(coordinate1[1] - coordinate2[1]))

    def threshold(self, polarRange1, polarRange2):
        return abs((polarRange1 - polarRange2) / (polarRange1 + polarRange2))
