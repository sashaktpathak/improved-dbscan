import itertools
import string
import math
import sys

def EuclideanDistance(point, centroid):
    result = 0

    result += pow(point.x - centroid.x, 2)
    result += pow(point.y - centroid.y, 2)

    result = math.sqrt(result)
    return result

def ManhattanDistance(point, centroid):
    result = 0

    result += abs(point.x - centroid.x)
    result += abs(point.y - centroid.y)

    return result

def Silhouette(clusters, m):
    res = []
    for index, cluster in enumerate(clusters):
        res2 = []
        for point in cluster.getPoints():
            a_i = GetA(point, cluster.getPoints(), m)
            b_i = GetB(point, clusters, m, index)
            res2.append(((b_i - a_i)/(max([a_i, b_i]))))

        clusterSum = 0
        for i in res2:
            clusterSum = clusterSum + i
        clusterAvg = clusterSum/len(res2)
        #print 'Silhouette Coefficient pro cluster ' + str(index) + ': ' + str(clusterAvg)
        res.append(clusterAvg)

    allSum = 0
    for i in res:
        allSum = allSum + i
    result = allSum/len(res)

    print 'Celkovy Silhouette Coefficient: ' + str(result)
    return result

def GetA(point, points, m):
    sum = 0
    for i in points:
        sum += m[point.index][i.index]

    t = len(points)-1
    if t != 0: 
        result = sum/t
    else: 
        result = 0
    return result


def GetAvgToCluster(point, cluster, m):
    sum = 0
    for i in cluster.getPoints():
        sum = sum + m[point.index][i.index]

    result = sum/cluster.getSize()
    return result

def GetB(point, clusters, m, c):
    results = []
    for index, cluster in enumerate(clusters):
        #netestuje se vlastni cluster
        if index == c: continue
        results.append(GetAvgToCluster(point, cluster, m))

    result = 0
    if(len(results) != 0): result = min(results)
    return result


def SumOfSquares(clusters, centroids, type):
    sum = 0
    for i, cluster in enumerate(clusters):
        for point in cluster.getPoints():
            if type == 'E': sum += EuclideanDistance(point, centroids[i])
            elif type == 'M': sum += ManhattanDistance(point, centroids[i])

    print 'Sum of squares(SSE): ' + str(sum)
    return sum;

def DunnIndex(clusters, centroids, type):
    distInCluster = []
    for i, cluster in enumerate(clusters):
        sum = 0
        for point in cluster.getPoints():
            if type == 'E': sum += EuclideanDistance(point, centroids[i])
            elif type == 'M': sum += ManhattanDistance(point, centroids[i])
        distInCluster.append((sum/cluster.getSize()))

    maxDistInCluster = max(distInCluster)
    
    distClusters = []
    for i1, c1 in enumerate(centroids):
        for i2, c2 in enumerate(centroids):
            if i1 == i2: break
            dist = 0
            if type == 'E': dist = EuclideanDistance(c1, c2)
            elif type == 'M': dist = ManhattanDistance(c1, c2)
            distClusters.append(dist)

    minDistClusters = 0
    if len(distClusters) != 0: minDistClusters = min(distClusters)

    result = minDistClusters/maxDistInCluster
    print 'Dunn index: ' + str(result)
    return result

def printSizeOfClusters(clusters):
    i = 0	
    #for idx, cluster in enumerate(clusters):
        #print 'Cluster ' + str(idx) + ': ' + str(cluster.getSize()) + ' points'
	
