import csv
import itertools
import string
import math
from timeit import default_timer as timer
import matplotlib.pyplot as plt
import random
import time
import sys
import validations

print ('cv6')
listp = [];
arguments = sys.argv[1]

FILENAME = 'datasets/clusters3.csv'
DELIM = ';'

EPS_ = 0
EPS = 2.5
MIN_PTS = 2

try:
    if "-f" in arguments:
        index = arguments.index("-f")
        FILENAME = arguments[index + 1]
    if "-eps" in arguments:
        index = arguments.index("-eps")
        EPS = int(arguments[index + 1])
    if "-min" in arguments:
        index = arguments.index("-min")
        MIN_PTS = int(arguments[index + 1])
except:
    print ('Argument error')


dataset = []
points = []

def plot(clusters, i):
    print ('Plotting..')
    #min, max
    maxx = 0
    minx = 0
    maxy = 0
    miny = 0
    for cluster in clusters:
        if cluster == None: continue
        for point in cluster.getPoints():
            if point.x < minx:
                minx = point.x
            if point.x > maxx:
                maxx = point.x
            if point.y < miny:
                miny = point.y
            if point.y > maxy:
                maxy = point.y

    for index, cluster in enumerate(clusters):
        #cluster
        if cluster == None: continue
        c = "#%06x" % random.randint(0, 0xFFFFFF)
        for point in cluster.getPoints():
            #plt.plot([point[0]], [point[1]], colors[index] + 'o')
            plt.plot([point.x], [point.y], color=c, marker='o')

    for p in points:
        if p.GetType() == 'NOISE':
            plt.plot([p.x], [p.y], color='#000000', marker='x')

    plt.draw()
    plt.axis([minx-1, maxx+1, miny-1, maxy+1])
    #plt.savefig('img' + str(i) + '.png', dpi=200)
    plt.show()

def EuclideanDistance(p1, p2):
    result = 0
    result += pow(p1.x - p2.x, 2)
    result += pow(p1.y - p2.y, 2)

    result = math.sqrt(result)
    return result

def ManhattanDistance(p1, p2):
    result = 0
    result += abs(p1.x - p2.x)
    result += abs(p1.y - p2.y)

    return result

class Point:
    def __init__(self, i, x, y):
        self.index = i
        self.x = x
        self.y = y
        self.visited = False
        self.type = ''
        self.inCluster = False

    def __repr__(self):
        return str(self.index) + ': (' + str(self.x) + ', ' + str(self.y) + ')' 

    def SetVisited(self):
        self.visited = True

    def IsVisited(self):
        return self.visited

    def GetType(self):
        return self.type

    def SetType(self, type):
        if type == 'CORE' or type == 'NOISE' or type == 'BORDER':
            self.type = type

class Cluster:
    def __init__(self):
        self.points = []

    def __repr__(self):
        return str(points)

    def addPoint(self, point):
        point.inCluster = True
        self.points.append(point);

    def getPoints(self):
        return self.points

    def getSize(self):
        return len(self.points)

    

def getDistanceMatrix(points):
    print ("dist.matrix...")
    matrix = [[0 for x in range(len(points))] for x in range(len(points))] 
    for i in range(len(points)):
        for j in range(len(points)):
            if i == j: break
            matrix[i][j] = EuclideanDistance(points[i], points[j])
            matrix[j][i] = matrix[i][j]

    return matrix

def expandClusterOld(corePoint, neighbours, cluster, eps, minPts, distanceMatrix):
    cluster.addPoint(corePoint)
    for p in neighbours:
        if p.IsVisited() != True:
            p.SetVisited()
            newNeighbours = regionQuery(distanceMatrix, p, eps)
            if len(newNeighbours) >= minPts:
                p.SetType('CORE')
                for i in newNeighbours:
                    neighbours.append(i)

        if p.inCluster != True:
            p.SetType('BORDER')
            cluster.addPoint(p)

    return cluster

def expandClusterNew(corePoint, neighbours, cluster, eps, minPts, distanceMatrix, eps_, clusters):
    if corePoint not in  cluster.getPoints():
        cluster.addPoint(corePoint)
        for p in neighbours:
            if p not in cluster.getPoints():
                cluster.addPoint(p)
            p.SetVisited()
        newNeighbours = regionQueryNew(distanceMatrix, corePoint, eps, eps_)
        for p in newNeighbours:
            status = 0
            if p.IsVisited() != True:
                p.SetVisited()
                neighbourCheck = regionQuery(distanceMatrix, p ,eps)
                if len(neighbourCheck) >= minPts:
                    p.SetType('CORE')
                    for pcheck in neighbourCheck:
                        clusterList = set(cluster.getPoints())
                        if pcheck in clusterList and len(regionQuery(distanceMatrix, pcheck, eps)) >= minPts:
                            status = 1
                            break
                if status == 1:
                    for pcheck in neighbourCheck:
                        if pcheck not in cluster.getPoints():
                            cluster.addPoint(pcheck)
                        pcheck.SetVisited()
                    newNeighbours2 = regionQueryNew(distanceMatrix, p, eps, eps_)
                    for pcheck in newNeighbours2:
                        if pcheck not in newNeighbours:
                            newNeighbours.append(pcheck)
                    
                else:
                    cluster1 = Cluster()
                    cluster1 = expandClusterNew(p, neighbourCheck, cluster1, eps, minPts , distanceMatrix, eps_, clusters)
                    clusters.append(cluster1);
        return cluster


def regionQuery(distanceMatrix, point, eps):
    neighbours = []
    for p_index, distance in enumerate(distanceMatrix[point.index]):
        if distance <= eps:
            neighbours.append(points[p_index])

    return neighbours

def regionQueryNew(distanceMatrix, point, eps, eps_):
    neighbours = []
    for p_index, distance in enumerate(distanceMatrix[point.index]):
        if distance >= eps and distance <= eps_:
            neighbours.append(points[p_index])

    return neighbours

def DBSCAN(eps, eps_ , minPts):
    clusters = []
    distanceMatrix = getDistanceMatrix(points)

    for point in points:
        if point.IsVisited(): continue
        point.SetVisited()
        neighbours = regionQuery(distanceMatrix, point, eps)
        if len(neighbours) < minPts:
            point.SetType('NOISE')
        else:
            point.SetType('CORE')
            cluster = Cluster()
            cluster = expandClusterNew(point, neighbours, cluster, eps, minPts, distanceMatrix, eps_, clusters)
            clusters.append(cluster)
            #print "New cluster: " + str(cluster.getSize()) + ' points.'

    result_silhouette = validations.Silhouette(clusters, distanceMatrix);

    centroids = []
    for idx, c in enumerate(clusters):
        sum_x = 0
        sum_y = 0
        for p in c.getPoints():
            sum_x += p.x
            sum_y += p.y
        centroids.append(Point(0, (sum_x/c.getSize()), (sum_y/c.getSize())))
    
    validations.SumOfSquares(clusters, centroids, 'E')
    validations.DunnIndex(clusters, centroids, 'E')
    validations.printSizeOfClusters(clusters);
    return clusters

def get_data2():
    data = []
    with open(FILENAME, 'rt') as file_obj:
        csv_reader = csv.reader(file_obj)
        for id_, row in enumerate(csv_reader):
            points.append(Point(id_, float(row[0]), float(row[1])))
    #return data
                   
def get_data():
    with open(FILENAME, 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=DELIM)
        for row in reader:
            tmp = []
            for number in row:
                tmp.append(float(number))
            dataset.append(tmp)

    for index, point in enumerate(dataset):
        points.append(Point(index, point[0], point[1]))
    
def main():
    EPS_ = float(sys.argv[1])
    countIter = 0
    get_data()   
    start = time.time()
    clusters = DBSCAN(EPS,EPS_, MIN_PTS)
    end = time.time()
    print(end-start)
    #res = DBSCAN(EPS,(EPS_+(i/10)), MIN_PTS)
    plot(clusters, 0)
main()

